from django.apps import AppConfig


class NewsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_app'

    def ready(self) -> None:
        # print(f'----- Hello: {__name__}')
        # if __name__ == 'main':
        from news_app.scheduler import scheduler
        print('Starting schedulers ---')
        scheduler.start()
        # pass
