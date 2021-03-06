#!/usr/local/bin/python3.3
# -*- coding: utf-8 -*-


class Site:

    def get_all_project_names(self):
        import configparser
        config = configparser.ConfigParser()
        config.read('all_projects.cfg', encoding='utf-8')
        return config.sections()

    def get_bool_parametr_from_projects_cfg(self, project_name, parametr):
        import configparser
        config = configparser.ConfigParser()
        config.read('all_projects.cfg', encoding='utf-8')
        return bool(config[project_name][parametr])

    def get_site_link(self, project_name):
        import configparser
        config = configparser.ConfigParser()
        config.read('all_projects.cfg', encoding='utf-8')
        site_link = config[project_name]['url']
        return site_link

    def get_site_content(self, project_name):
        import requests
        site_link = self.get_site_link(project_name)
        site_content = requests.get(site_link).text.splitlines()
        return site_content

    def get_rows_count(self, content):
        rows_count = len(content)
        return rows_count

    def get_number_of_max_rows(self, project_name, site_content):
        cache = Cache()
        cache_text = cache.get_site_cache(project_name)
        if len(site_content) > len(cache_text):
            number_of_max_row = len(cache_text)
        elif len(site_content) < len(cache_text):
            number_of_max_row = len(site_content)
        else:
            number_of_max_row = len(site_content)
        return number_of_max_row

    def get_status_code_of_site(self, project_name):
        import requests
        import time
        link = self.get_site_link(project_name)
        site = requests.get(link)
        site_status_code = site.status_code
        if site_status_code != 200:
            time.sleep(60)
            site_status_code = site.status_code
            return site_status_code
        return site_status_code

    def does_site_have_cache(self, project_name):
        filename = '{0}.cache'.format(project_name)
        dir_name = 'cache'
        try:
            file = open('{0}/{1}'.format(dir_name, filename),
                        'r', encoding='utf-8')
            file.close
            return True
        except:
            return False

    def is_it_first_load_of_project(self, project_name):
        try:
            file = 'cache/{0}.cache'.format(project_name)
            open(file, 'r')
            return False
        except:
            return True

    def how_much_hrefs_on_site(self, project_name):
        import re
        site_content = self.get_site_content(project_name)
        find_href = re.compile('href=\S*')
        href_count = 0
        for line in site_content:
            href_count += len(find_href.findall(line))
        return href_count

    def find_all_hrefs_on_site(self, project_name):
        import re
        find_href = re.compile('href=\S*')
        site = self
        site_content = site.get_site_content(project_name)
        list_of_hrefs_on_site = []
        for line in site_content:
            hrefs_in_line = find_href.findall(line)
            if hrefs_in_line:
                for href in hrefs_in_line:
                    list_of_hrefs_on_site.append(href)
        return list_of_hrefs_on_site

    def get_status_in_str_off_all_projects(self):
        site = Site()
        all_project_names = site.get_all_project_names()
        msg = ''
        for project_name in all_project_names:
            site_status_code = site.get_status_code_of_site(project_name)
            msg = ('{0}{1} status: {2}\n'
                   .format(msg, project_name, site_status_code))

        return msg


class Cache:

    def make_site_cache(self, project_name):
        import re
        site = Site()
        site_content = site.get_site_content(project_name)
        filename = '{0}.cache'.format(project_name)
        dir_name = 'cache'
        file = open('{0}/{1}'.format(dir_name, filename), 'w', encoding='utf-8')

        for line in range(0, len(site_content)):
            file.write('{0}\n'.format(str(site_content[line])))
        file.close

        find_href = re.compile('href=\S*')
        count_href_in_cache = 0
        for line in site_content:
            count_href_in_cache += len(find_href.findall(line))

    def make_sites_caches(self):
        site = Site()
        for project_name in Site.get_all_project_names(self):
            site_content = site.get_site_content(project_name)
            self.make_site_cache(project_name, site_content)

    def get_site_cache(self, project_name):
        filename = '{0}.cache'.format(project_name)
        dir_name = 'cache'
        file = open('{0}/{1}'.format(dir_name, filename),
                     'r', encoding='utf-8')
        cache_text = []

        for line in file:
            cache_text.append(line.strip('\n'))
        file.close
        return list(cache_text)

    def when_does_chache_maked(self, project_name):
        import re
        find_date = re.compile('\d\S*\d')
        cache_text = self.get_site_cache(project_name)
        when_does_chache_maked = find_date.findall(cache_text[0])
        return when_does_chache_maked[0]

    def how_much_hrefs_in_cache(self, project_name):
        import re
        cache_content = self.get_site_cache(project_name)
        find_href = re.compile('href=\S*')
        href_count = 0
        for line in cache_content:
            href_count += len(find_href.findall(line))
        return href_count

    def find_all_hrefs_in_cache(self, project_name):
        import re
        find_href = re.compile('href=\S*')
        cache = self
        cache_content = cache.get_site_cache(project_name)
        list_of_hrefs_in_cache = []
        for line in cache_content:
            hrefs = find_href.findall(line)
            if hrefs:
                for href in hrefs:
                    list_of_hrefs_in_cache.append(href)
        return list_of_hrefs_in_cache


class Difference:

    def row_difference_to_list(self, project_name):

        difference_row_list = []
        difference_row = []
        difference_count = False
        min_max = []
        site = Site()
        cache = Cache()
        site_content = site.get_site_content(project_name)
        site_cache = cache.get_site_cache(project_name)
        max_rows = site.get_number_of_max_rows(project_name, site_content)
        for row in range(0, max_rows):
            if site_content[row] != site_cache[row]:
                difference_row.append((row + 1))
                difference_count = True
            elif site_content[row] == site_cache[row] and difference_count == True:
                if len(difference_row) > 1:
                    difference_count = False
                    row_min = min(difference_row)
                    row_max = max(difference_row)
                    min_max.append(row_min)
                    min_max.append(row_max)
                    difference_row_list.append(min_max)
                    min_max = []
                    difference_row = []
                elif len(difference_row) == 1:
                    difference_row_list.append(difference_row)
                    difference_row = []
                else:
                    continue
            else:
                continue

        return difference_row_list

    def chek_for_href_count_change(self, project_name):

        site = Site()
        cache = Cache()
        all_hrefs_on_site = site.find_all_hrefs_on_site(project_name)
        all_hrefs_on_cache = cache.find_all_hrefs_in_cache(project_name)
        new_hrefs = []
        for href in all_hrefs_on_site:
            if href in all_hrefs_on_cache:
                continue
            else:
                new_hrefs.append(href)

        if len(new_hrefs) == 0:
            return 'OK'
        else:
            return 'Something wrong'

    def find_new_hrefs_on_site(self, project_name):
        site = Site()
        cache = Cache()

        all_hrefs_on_site = site.find_all_hrefs_on_site(project_name)
        all_hrefs_on_cache = cache.find_all_hrefs_in_cache(project_name)
        new_hrefs = []
        for href in all_hrefs_on_site:
            if href in all_hrefs_on_cache:
                continue
            else:
                new_hrefs.append(href)

        return new_hrefs


class Twitter:

    def make_post_to_twitter_from_str(self, msg):
        import configparser
        from twython import Twython
        import random

        random = random.randrange(1, 999)

        twitter_ini = configparser.ConfigParser()
        twitter_ini.read('site_cheker.cfg')

        OAUTH_TOKEN = twitter_ini['twitter']['OAUTH_TOKEN']
        OAUTH_TOKEN_SECRET = twitter_ini['twitter']['OAUTH_SECRET']
        APP_KEY = twitter_ini['twitter']['CONSUMER_KEY']
        APP_SECRET = twitter_ini['twitter']['CONSUMER_SECRET']
        acc_to_push = twitter_ini['twitter']['acc_to_push']

        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        msg = '{0} {1} {2}'.format(random, acc_to_push, msg)
        twitter.update_status(status=msg)


class Config:

    def get_setting_of_sitecheker(self, setting):
        import configparser
        sitecheker_cfg = configparser.ConfigParser()
        sitecheker_cfg.read('site_cheker.cfg')
        setting = sitecheker_cfg['site cheker'][setting]

        return setting


class SMS:

    def send_sms(self, msg):
        pass


class LogFile:

    def write_to_start_of_log(self, log_msg):
        log_file = open('logs/main_log.html', 'r', encoding='utf-8')
        logs_in_list = log_file.readlines()
        log_msg += '\n'
        logs_in_list.insert(0, log_msg)
        log_file.close()
        log_file = open('logs/main_log.html', 'w', encoding='utf-8')
        log_file.writelines(logs_in_list)
        log_file.close()
