from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from JegBridge.auth.base_auth import BaseAuth


class HasAuthAndSeller(Protocol):
    auth: "BaseAuth"
    seller_id: str


class AmazonListingHandler:
    """
    Mixin providing Amazon listing-related API methods.
    Requires the host class to provide `self.auth` (BaseAuth) and `self.seller_id` (str).
    """

    def get_listing(self: "HasAuthAndSeller", sku: str) -> dict:
        """
        Get listing information for a given SKU.

        Args:
            sku (str): The seller SKU to look up.

        Returns:
            dict: The listing object as returned by the Amazon Listings API.

        Reference:
            https://developer-docs.amazon.com/sp-api/docs/listings-items-api-v2021-08-01-reference#getlistingsitem
        """
        endpoint = f"/listings/2021-08-01/items/{self.seller_id}/{sku}"
        params = {
            "marketplaceIds": "ATVPDKIKX0DER",
            "issueLocale": "en_US",
            "includedData": "fulfillmentAvailability,attributes,summaries"
        }
        response = self.auth.make_request("GET", endpoint=endpoint, params=params)
        return response.json()
