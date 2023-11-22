from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Create your views here.
class FootballMatchesAPIView(APIView):
    def get(self, request):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Buning orqali brauzerni ekranda ko'rsatmasdan ishga tushiramiz
        driver = webdriver.Chrome(options=chrome_options)
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


class FootballFinishedMatchAPIView(APIView):
    def get(self, request):
        # JSON formatida javobni qaytarish

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.flashscore.com/football/')

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        old_games = []

        game_elements = soup.find_all('div', class_='event__match--last')

        for game_element in game_elements:
            teams_element = game_element.find_all('div', class_='event__participant')
            team1 = teams_element[0].text.strip()
            team2 = teams_element[1].text.strip()

            score_home = game_element.find('div', class_='event__score event__score--home')
            score1 = '' if not score_home else score_home.text.strip()

            score_away = game_element.find('div', class_='event__score event__score--away')
            score2 = score_away.text.strip()

            game_info = {
                'team1': team1,
                'team2': team2,
                'score1': score1,
                'score2': score2,
            }

            old_games.append(game_info)

        driver.quit()
        return Response(old_games)
