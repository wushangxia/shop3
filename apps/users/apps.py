from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "用户管理"
    def ready(self):
        #现在添加用户的时候，密码就会自动加密存储了
        import users.signals
        print(12)
