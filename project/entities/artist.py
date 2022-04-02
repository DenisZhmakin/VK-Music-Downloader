from bs4 import BeautifulSoup


class VkArtist:
    def __init__(self, html: str):
        self._nickname = VkArtist._parse_nickname(html)

    @staticmethod
    def _parse_nickname(html: str):
        """bfxbx"""
        if "OwnerRow OwnerRow_artist al_artist" in html:
            soup = BeautifulSoup(html, 'html.parser')
            artist = soup.find('div', {'class': 'OwnerRow OwnerRow_artist al_artist'})
            sub_link = artist.find('a', {'class': 'OwnerRow__content'})['href']

            return sub_link.split('/')[-1]

        return ""

    @property
    def nickname(self):
        return self._nickname