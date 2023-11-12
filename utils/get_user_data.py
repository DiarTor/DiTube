import logging

from bot.database import users_collection


class UserDataProvider:
    def __init__(self, user_id):
        """
        Initialize UserDataProvider with a user_id.

        :param user_id:
        The unique identifier for the user.
        """

        self.user_id = user_id
        self.user = self._get_user_data()

    def _get_user_data(self) -> dict:
        """
        Retrieve user data from the database.

        Returns :
        - dict: User data if found, None otherwise.
        """

        try:
            user_data = users_collection.find_one({"user_id": self.user_id})
            return user_data
        except Exception as e:
            logging.error(f"Error retrieving user data: {e}")
            return None

    def get_user_language(self) -> str:
        """
        Get the language setting for the user.

        Returns :
        - not_selected (str): if the user did'nt select a language.
        - fa (str): if the user selected Farsi(persian).
        - en (str): if the user selected English.
        """

        if self.user:
            return self.user['settings']['language']
        else:
            return "not_selected"

    def get_user_subscription_details(self) -> dict:
        """
        Get details about the user's subscription.

        Returns :
        - dict: Subscription details.
        """

        if self.user:
            return self.user.get("subscription", {})
        else:
            return {}

    def return_response_based_on_language(self, english=None, persian=None) -> str:
        """
        Generate a response based on the user's language setting.

        Parameters :
        - english (str): The response in English.
        - persian (str): The response in Persian.

        Returns :
        - str: The response in the user's language.
        """

        user_language = self.get_user_language()
        response = english if user_language == "en" else persian
        return response
