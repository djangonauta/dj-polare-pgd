from allauth.account import adapter


class DisableSignupAdapter(adapter.DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return False
