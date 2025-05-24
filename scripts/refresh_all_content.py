from services.content.content_service import ContentService


def main():
    service = ContentService()
    service.delete_all_content()
    service.extract_and_save_all_pages_content()
    service.extract_and_save_all_posts_content()
    service.extract_and_save_all_products_content()


if __name__ == "__main__":
    main()
