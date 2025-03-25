import requests
from bs4 import BeautifulSoup

def scrape_favikon_tiktok_influencers():
    url = "https://www.favikon.com/blog/top-10-most-followed-tiktok-influencers"
    response = requests.get(url)
    response.encoding = 'utf-8'
    response.raise_for_status()  

    soup = BeautifulSoup(response.text, "html.parser")

    # Znajdź główny kontener
    main_div = soup.find("div", class_="rich-text-blog w-richtext")
    if not main_div:
        print("Nie znaleziono głównego kontenera z danymi (div.rich-text-blog.w-richtext).")
        return

    # Znajdź wszystkie <h3> wewnątrz main_div
    h3_tags = main_div.find_all("h3")

    with open("influencers.md", "w", encoding="utf-8") as f:
        f.write("# Here's the list of the Top 10 Most Followed TikTok Influencers in 2025 :\n\n")

        for h3 in h3_tags:
            # 1) Sprawdź, czy w tym <h3> jest link do tiktok.com
            a_tag = h3.find("a", href=lambda href: href and "tiktok.com" in href)
            if not a_tag:
                # Jeśli nie ma linku do TikToka, to pewnie nie jest to influencer
                continue

            # Wyciągnij nazwę (np. "Will Smith 🇺🇸")
            name_text = h3.get_text()
            tiktok_url = a_tag["href"]

            
            paragraphs = []
            next_el = h3.next_sibling
            while next_el:
                # Jeśli trafimy na kolejny <h3>, to kończymy
                if next_el.name == "h3":
                    break
                # Zapisujemy <p> do listy
                if next_el.name == "p":
                    paragraphs.append(next_el)
                next_el = next_el.next_sibling

            # 3) Przeanalizuj paragrafy – wyciągnij Followers, Score, AI Link i Opis
            followers = "?"
            score = "?"
            ai_profile_url = "?"
            description_parts = []

            for p in paragraphs:
                text = p.get_text(strip=True)

                if "Followers on TikTok" in text:
                    strong = p.find("strong")
                    if strong:
                        followers = strong.get_text(strip=True)
                elif "Favikon Authority Score" in text:
                    strong = p.find("strong")
                    if strong:
                        score = strong.get_text(strip=True)
                elif "AI Powered Profile" in text:
                    link = p.find("a", string=lambda s: "AI Powered Profile" in s)
                    if link:
                        ai_profile_url = link["href"]
                else:
                    # Zakładamy, że to opis
                    description_parts.append(text)

            description = "\n\n".join(description_parts) if description_parts else "Brak opisu"

            # 4) Zapisz do pliku .md
            f.write(f"## {name_text}\n\n")
            f.write(f"**TikTok:** {tiktok_url}\n\n")
            f.write(f"**Followers:** {followers}\n\n")
            f.write(f"**Favikon Authority Score:** {score}\n\n")
            f.write(f"**AI Powered Profile:** {ai_profile_url}\n\n")
            f.write(f"**Opis:** {description}\n\n")
            f.write("---\n\n")

    print("✅ Plik 'influencers.md' został wygenerowany.")

if __name__ == "__main__":
    scrape_favikon_tiktok_influencers()
