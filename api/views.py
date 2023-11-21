from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
from selenium import webdriver


# Create your views here.
class FlashScoreDataAPIView(APIView):
    def get(self, request):
        driver = webdriver.Chrome()
        try:
            driver.get("https://www.flashscore.com/football/")

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            matches = soup.find_all('div', class_='event__match')

            result_data = []

            for match in matches:
                time = match.find('div', class_='event__time')
                teams = match.find_all('div', class_='event__participant')
                team1, team2 = teams
                res = f"{str(time)[25:30]}: {team1.text} vs {team2.text}"
                if res[0] != ':':
                    result_data.append(res)

            return Response(result_data, status=status.HTTP_200_OK)

        finally:
            driver.quit()
