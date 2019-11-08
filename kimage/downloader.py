from pathlib import Path
import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests

class Downloader():
    """
    Class handling downloading images from list of URLs.
    """
    def __init__(self, website, chunk_size=1024):
        """
        Downloader constructor.
        """
        self.download_dir = Path(__file__).parent / 'database' / 'download'
        self.chunk_size = chunk_size
        self.website = website
    ### Public
    def download_from_list_of_urls(self, url_list):
        """
        Download images from a list of URLs.
        """
        time_start = time.time()
        n_images_downloaded = 0
        n_url = len(url_list)
        i_url = 0
        for url in url_list:
            progress = "Downloaded {0} images from {1}/{2} URLs ({3}%)".format(
                n_images_downloaded,
                i_url,
                n_url,
                int(i_url/n_url*100),
            )
            print(progress)
            n_images_downloaded += self._download_from_url(url)
            i_url += 1

        result = "Downloaded {0} images from {1} URLs".format(
            n_images_downloaded,
            n_url,
        )
        print(result)
        print("Process took {} seconds.".format(round(time.time() - time_start)))
        return
    def download_from_html(self):
        time_start = time.time()
        from naver_html import html
        image_url_list = []
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())
        tag_list = soup.find_all('img', attrs={
            # 'href': '#',
            # 'data-linktype': 'img',
            # 'class': 'se_mediaImage __se_img_el',
            })
        # tag_list = soup.find_all('img')
        # print(tag_list)
        for tag in tag_list:
            if "data-src" in tag.attrs:
                image_url = tag.attrs["data-src"]
                
                # print(image_url)

                string_cutoff_index = image_url.lower().find('?type=')
                print(image_url[:string_cutoff_index])
                image_url_list.append(image_url[:string_cutoff_index])







                ### Old code to strip out the "?type=w1200"
                # string_cutoff_index = image_url.lower().find('.jpg')
                # if string_cutoff_index > -1:
                #     image_url_list.append(image_url[:string_cutoff_index + 4])
                # else:
                #     string_cutoff_index = image_url.lower().find('.jpeg')
                #     if string_cutoff_index > -1:
                #         image_url_list.append(image_url[:string_cutoff_index + 5])
                #     else:
                #         print("Error: image url does not use .jpg or .jpeg")
                










        n_images_downloaded = self._download_images_from_image_urls(image_url_list)

        result = "Downloaded {0} images.".format(
            n_images_downloaded,
        )
        print(result)
        print("Process took {} seconds.".format(round(time.time() - time_start)))
        return
    ### Private
    def _download_from_url(self, url):
        """
        Downloads images from a single URL.
        Returns the number of images downloaded.
        """
        n_images_downloaded = 0
        url = self._process_url(url)

        # Get reponse from URL using html-requests
        response = HTMLSession().get(url)

        # Break for this URL because error in request/response
        if response.status_code != 200:
            print("HTML response status code {0} for {1}".format(
                response.status_code,
                url,
            ))
        else:
            # Get image URLs from response HTML tags
            soup = BeautifulSoup(response.content, 'lxml')
            # print(soup)
            image_url_list = self._get_image_urls_from_soup(soup)
            if not image_url_list:
                print("URL has no images:", url)
            else:
                n_images_downloaded = self._download_images_from_image_urls(image_url_list)
        return n_images_downloaded
    def _process_url(self, url):
        """
        Preprocesses the URL string.
        """
        # Strip whitespace (mainly the \n and \n newline)
        url = url.rstrip()
        # Transform mobile version of links
        url = url.replace("mobile.", "")
        return url
    def _get_image_urls_from_soup(self, soup):
        """
        Returns a list of image URL strings from the HTML soup.
        """
        image_url_list = []
        if self.website == "Twitter":
            tag_list = soup.find_all('img')
            for tag in tag_list:
                if 'src' in tag.attrs:
                    src_url = tag.attrs['src']
                    if 'https://pbs.twimg.com/media/' in src_url:
                        image_url = src_url + ':orig'
                        image_url_list.append(image_url)
                        # print(image_url)
            ### Old way to get images. Only gets large size, not original size.
            # tag_list = soup.find_all('meta', property='og:image')
            # for tag in tag_list:
            #     if 'content' in tag.attrs:
            #         image_url = tag.attrs['content']
            #         if 'jpg:large' in image_url:
            #             image_url_list.append(image_url)
        elif self.website == "Naver":
            tag_list = soup.find_all('a', href="#")
            for tag in tag_list:
                if 'href' in tag.attrs:
                    print(tag)
        return image_url_list
    def _download_images_from_image_urls(self, image_url_list):
        """
        Downloads the images from the image URLs.
        Returns the number of successfully downloaded images.
        """
        naver_image_index = 1
        n_images_downloaded = 0
        # print(image_url_list)
        for image_url in image_url_list:
            # print(image_url)
            if self.website == "Twitter":
                # Split image_URL using / and get image file name
                image_file_name = image_url.split('/')[-1]
                # image_file_name = image_file_name.replace("jpg:large", "jpg")
                image_file_name = image_file_name.replace("jpg:orig", "jpg")
                download_file_path = self.download_dir / image_file_name
            elif self.website == "Naver":
                image_file_name = str(naver_image_index) + ".jpg"
                download_file_path = self.download_dir / image_file_name
                naver_image_index += 1
            else:
                print("Website not selected at time of image download!")
                break




            # Check that image file name is not already in destination folder
            if download_file_path.is_file():
                print("Already exists:", str(download_file_path))
            else:
                # Get image from image URL
                image_response = requests.get(image_url, stream=True)
                if image_response.status_code != 200:
                    print("Error: Response code {0} for {1}".format(
                        image_response.status_code,
                        image_url
                    ))
                else:
                    # Write image data to disk using the set download chunk size
                    with download_file_path.open(mode='wb') as f:
                        for chunk in image_response.iter_content(self.chunk_size):
                            f.write(chunk)
                    n_images_downloaded += 1
        return n_images_downloaded
