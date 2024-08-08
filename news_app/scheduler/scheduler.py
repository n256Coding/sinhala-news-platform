from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.job import Job
from django_apscheduler.jobstores import register_events, DjangoJobStore
import sys

from news_app.models import News
from news_app.services.classifier import Classifier
from news_app.services.spider import Spider
from recommendation.services.vector_db_provider import get_chroma_db_collection

def my_scheduled_task(scheduler):

    # Get all jobs
    jobs = scheduler.get_jobs()
    
    # Print job IDs and the number of jobs
    for job in jobs:
        print(f'Job ID: {job.id}')
    print(f'Number of current jobs: {len(jobs)}')


    print(f"{Job.id} Task is running...")

    classifier = Classifier()
    spider = Spider()
    chroma_collection = get_chroma_db_collection()

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

        chroma_collection.add(
            ids=[classifed_news_item.news_id],
            embeddings=[classifed_news_item.get_content_embedding()],
            metadatas=[{'timestamp': classifed_news_item.get_posix_timstamp()}]
        )

        
    
    print(f'{Job.id} Task completed')

def start():

    # 10 seconds delay to start the scheduler after app is started
    # time.sleep(10)
    

    scheduler = BackgroundScheduler(
        gconfig = {
            'apscheduler.job_defaults.max_instances': 1
        }
    )
    # scheduler.add_jobstore(DjangoJobStore(), "default")
    # scheduler.add_jobstore(MemoryJobStore(), 'inmemory')
    print(f'Current jobs: {scheduler.get_jobs()}')

    if scheduler.running:
        scheduler.shutdown(False)
        scheduler.start(False)
    
    scheduler.remove_all_jobs()
    scheduler.add_job(my_scheduled_task, 
                      'interval', 
                      seconds=300, 
                      name='my_task_1', 
                    #   jobstore='inmemory',
                      max_instances=1,
                      args=[scheduler]
                      )
    register_events(scheduler)
    scheduler.start()
    print(f"Scheduler started...", file=sys.stdout)
