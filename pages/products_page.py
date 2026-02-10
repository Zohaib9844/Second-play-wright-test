from pages.base_page import BasePage


class ProductsPage(BasePage):
    # Selectors
    SEARCH_INPUT = 'input#search_product'
    SEARCH_BUTTON = 'button#submit_search'
    PRODUCT_NAMES = '.productinfo h2'
    PRODUCT_CARDS = '.features_items .col-sm-4'
    ALL_PRODUCTS_HEADING = 'h2.title.text-center'

    def navigate_to_products(self):
        self.navigate("/products")

    def search(self, keyword: str):
        self.page.fill(self.SEARCH_INPUT, keyword)
        self.page.click(self.SEARCH_BUTTON)
        self.page.wait_for_selector(self.PRODUCT_NAMES, timeout=7000)

    def get_product_names(self) -> list[str]:
        """Return list of all visible product name strings."""
        elements = self.page.locator(self.PRODUCT_NAMES).all()
        return [el.text_content().strip() for el in elements]

    def get_product_count(self) -> int:
        return self.page.locator(self.PRODUCT_CARDS).count()

    def is_products_page(self) -> bool:
        return self.page.is_visible(self.ALL_PRODUCTS_HEADING)