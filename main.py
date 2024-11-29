from restaurant_crawler import RestaurantInfo
from post_generator import PostGenerator

def main() :
    restaurant=RestaurantInfo("버우드","연남")
    info=restaurant.crawling_restaurant()
    
    GOOGLE_API_KEY = 'AIzaSyBiKq7ZZp_Rndr7IA6K0_2ZeGrwJeWUqxI'
    postgen = PostGenerator(info,['베이컨 에그 베네딕트','단호박 뇨끼','체리 에이드','케일 시금치 사과 주스'],'2024-02-04',GOOGLE_API_KEY)
    
    title = postgen.generate_title()
    post = postgen.generate_post()
    schedule = postgen.generate_schedule()
    
    return title, post, schedule


if __name__ == "__main__" :
    a, b, c = main()
    
    print(a)
    print(b)
    print(c) 
    