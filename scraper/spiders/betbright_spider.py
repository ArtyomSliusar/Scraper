import scrapy
from scraper.items import RaceItem, ParticipantItem


class BetbrightSpider(scrapy.Spider):
    name = "betbright_horse_races"
    custom_settings = {
        'FEED_EXPORT_FIELDS': ["track_name", "race_id", "race_time", "participants"],
        'ITEM_PIPELINES': {
            'scraper.pipelines.WriteToCsv': 999,
        }
    }
    start_urls = ['https://www.betbright.com/horse-racing/today']

    def parse(self, response):
        tracks = response.xpath('//table[@class="racing"]//tr[descendant::td]')
        for track in tracks:
            track_url = (track.css('a::attr(href)').extract_first())
            yield scrapy.Request(track_url, self.parse_tracks)

    def parse_tracks(self, response):
        items = []
        races = response.css('div.inner_container ul.racecard')
        for race in races:
            item = RaceItem()
            event_name = race.css('div.event-name::text').extract_first()
            time_name = event_name.split(' ', 1)
            item['race_time'] = time_name[0]
            item['track_name'] = time_name[1]
            item['race_id'] = race.css('::attr(data-event-id)').extract_first()
            item['participants'] = self.parse_participants(race, item['race_id'])
            items.append(item)
        return items

    def parse_participants(self, race, id):
        items = []
        participants = race.css('li#racecard_{}_tab_winmarket ul.horses-list li.horse-container'.format(id))
        for participant in participants:
            item = ParticipantItem()
            item['participant_name'] = participant.css('div.horse-information-name::text').extract_first()
            item['participant_id'] = participant.css('ul.horse::attr(data-participant-id)').extract_first()
            selection_id = participant.css('li.field-win-ew a::attr(data-selection-id)').extract_first()
            item['participant_chances'] = participant.css('a#selection_id_{}::text'.format(selection_id)).extract_first()
            items.append(item)
        return items