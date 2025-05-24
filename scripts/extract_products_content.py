from services.content.content_service import ContentService


def main():
    service = ContentService()
    service.extract_and_save_all_products_content()


if __name__ == "__main__":
    main()
