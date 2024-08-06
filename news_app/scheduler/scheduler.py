from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys

from news_app.models import News
from news_app.services.classifier import Classifier
from news_app.services.spider import Spider

def my_scheduled_task():

    print("Task is running...")

    classifier = Classifier()
    spider = Spider()

    news_items = spider.load_latest_news_items()

    classified_news_items = classifier.classify(news_items)

    for classifed_news_item in classified_news_items:

        print(f'Saving news id: {classifed_news_item.news_id}, Category: {classifed_news_item.category}')

        news_model = News(
            news_id = classifed_news_item.news_id,
            date = classifed_news_item.timestamp,
            heading = classifed_news_item.heading,
            category = classifed_news_item.category,
            link_to_source = classifed_news_item.link_to_source
        )

        news_model.save()
    
    print('Task completed')

def start():

    # 10 seconds delay to start the scheduler after app is started
    # time.sleep(10)
    

    scheduler = BackgroundScheduler(
        # executors = {
        #     'default': ThreadPoolExecutor(max_workers=1),
        #     'processpool': ProcessPoolExecutor(1)
        # }
        # gconfig = {
        #     'executors': 1
        # },
        gconfig = {
            'apscheduler.job_defaults.max_instances': 1
        }
    )
    # scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.remove_all_jobs()
    scheduler.add_job(my_scheduled_task, 
                      'interval', 
                      seconds=60, 
                      name='my_task_2', 
                      jobstore='default',
                      max_instances=1,
                      )
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)
