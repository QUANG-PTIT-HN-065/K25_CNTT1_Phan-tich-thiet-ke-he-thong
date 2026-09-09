import time

def process_rikkeimart_order(item_status, customer_response):
    """
    Mô phỏng luồng xử lý đơn hàng RikkeiMart khi tài xế đến cửa hàng.
    """
    try:
        print(f"\n--- BẮT ĐẦU XỬ LÝ ĐƠN HÀNG RIKKEIMART ---")
        
        # 1. Kiểm tra trạng thái món hàng tại cửa hàng
        if item_status == "AVAILABLE":
            print("[Tài xế]: Đã tìm thấy đủ thực phẩm. Tiến hành mua hàng và giao cho khách.")
            return {
                "status": "SUCCESS",
                "action": "DELIVER_ORIGINAL_ITEM",
                "message": "Đơn hàng hoàn tất với sản phẩm ban đầu."
            }
        
        elif item_status == "OUT_OF_STOCK":
            print("[Cảnh báo]: Thực phẩm đã HẾT HÀNG tại cửa hàng!")
            print("[Tài xế]: Chọn 'Đề xuất sản phẩm thay thế tương đương' trên App.")
            print("[Hệ thống]: Đã gửi thông báo xác nhận đổi món tới App Khách hàng.")
            print("[Hệ thống]: Kích hoạt đếm ngược Timeout 3 phút để chờ phản hồi...")
            
            time.sleep(0.5) # Giả lập chờ tín hiệu
            
            # 2. Xử lý kịch bản dựa trên phản hồi của Khách hàng
            if customer_response == "ACCEPT":
                print("[Khách hàng]: Đã bấm ĐỒNG Ý đổi sản phẩm thay thế.")
                print("[Tài xế]: Mua sản phẩm thay thế và tiếp tục giao hàng.")
                return {
                    "status": "SUCCESS",
                    "action": "DELIVER_SUBSTITUTE_ITEM",
                    "message": "Đơn hàng hoàn tất với sản phẩm thay thế."
                }
                
            elif customer_response == "REJECT":
                print("[Khách hàng]: TỪ CHỐI sản phẩm thay thế.")
                print("[Hệ thống]: Hủy đơn hàng theo yêu cầu khách hàng và hoàn tiền.")
                return {
                    "status": "CANCELLED_BY_CUSTOMER",
                    "action": "CANCEL_AND_REFUND",
                    "message": "Đơn hàng đã hủy an toàn do khách hàng không đồng ý đổi món."
                }
                
            elif customer_response == "TIMEOUT":
                # BẪY MẤT LIÊN LẠC (Unreachable Customer Trap)
                print("[Cảnh báo - Bẫy Timeout]: Khách hàng KHÔNG PHẢN HỒI sau 3 phút!")
                print("[Hệ thống]: Tự động ngắt mạch Timeout 3 phút (Safe Auto-cancel) để giải phóng Tài xế.")
                return {
                    "status": "AUTO_CANCELLED_TIMEOUT",
                    "action": "RELEASE_DRIVER_AND_NOTIFY",
                    "message": "Hệ thống tự động hủy đơn an toàn do Hết giờ chờ (Timeout 3m). Giải phóng tài xế."
                }
            else:
                raise ValueError(f"Phản hồi của khách hàng không hợp lệ: '{customer_response}'")
                
        else:
            raise ValueError(f"Trạng thái sản phẩm không hợp lệ: '{item_status}'")
            
    except Exception as e:
        # Bắt trọn ngoại lệ để chương trình không bị crash
        print(f"[Xử lý ngoại lệ]: Phát hiện lỗi hệ thống -> {e}")
        return {
            "status": "SYSTEM_ERROR",
            "action": "LOG_ERROR",
            "message": f"Hệ thống xử lý an toàn ngoại lệ: {e}"
        }

# KIỂM THỬ CÁC KỊCH BẢN (TEST CASES)
if __name__ == "__main__":
    # Case 1: Món hàng còn đủ
    res1 = process_rikkeimart_order(item_status="AVAILABLE", customer_response=None)
    print("Kết quả:", res1)

    # Case 2: Hết hàng -> Khách đồng ý đổi
    res2 = process_rikkeimart_order(item_status="OUT_OF_STOCK", customer_response="ACCEPT")
    print("Kết quả:", res2)

    # Case 3: Hết hàng -> Bẫy Timeout 3 phút (Khách không nghe máy/không phản hồi)
    res3 = process_rikkeimart_order(item_status="OUT_OF_STOCK", customer_response="TIMEOUT")
    print("Kết quả:", res3)

    # Case 4: Dữ liệu lỗi/Ngoại lệ bất ngờ (Đảm bảo chương trình không crash)
    res4 = process_rikkeimart_order(item_status="OUT_OF_STOCK", customer_response="INVALID_INPUT")
    print("Kết quả:", res4)