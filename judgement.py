# -*- coding: utf-8 -*-
# @Time : 2019/4/11 10:23
# @Author : Vanya
import math
from PIL import Image, ImageChops


class Judgement(object):
    @staticmethod
    def is_same(image1, image2, threshold=100):
        diff = ImageChops.difference(image1, image2)
        if diff.getbbox() is None:
            return True
        else:
            diff_count = math.sqrt(sum([x*2 for x in diff.getdata()]))
            print(diff_count)
            if diff_count < threshold:
                return True
            # diff.save('diff.png')

    def is_reward_continue_page(self, pic):
        im = Image.open(pic)
        im = im.convert('L')
        im = im.crop((650, 570, 770, 670))
        im2 = Image.open('standard/reward.png')
        return self.is_same(im, im2)

    def find_can_challenge_pos(self, pic):
        right_positions = [521, 908, 1294]
        top_positions = [104, 256, 408]
        im = Image.open(pic)
        im = im.convert('L')
        im2 = Image.open('standard/challenge1.png')
        for top in top_positions:
            for right in right_positions:
                im1 = im.crop((right-50, top, right, top+50))
                if self.is_same(im1, im2, 200):
                    return top, right

    def is_challenge_in_page(self, pic, top, right):
        im = Image.open(pic)
        im = im.convert('L')
        im = im.crop((right-128, top+245, right-28, top+295))
        im2 = Image.open('standard/challenge2.png')
        return self.is_same(im, im2, 300)

    def is_refresh_ok(self, pic):
        im = Image.open(pic)
        im = im.convert('L')
        im = im.crop((850, 450, 950, 500))
        im2 = Image.open('standard/challenge_refresh.png')
        return self.is_same(im, im2, 300)

    def is_failed(self, pic):
        im = Image.open(pic)
        im = im.convert('L')
        im = im.crop((430, 560, 500, 600))
        im2 = Image.open('standard/failed.png')
        return self.is_same(im, im2, 300)

    def is_yuhun_challenge_in_page(self, pic):
        im = Image.open(pic)
        im = im.convert('L')
        im = im.crop((1041, 528, 1141, 578))
        im2 = Image.open('standard/yh.png')
        return self.is_same(im, im2, 300)


def just_test():
    im = Image.open('pics/yh1.png')
    im = im.convert('L')
    im1 = im.crop((1041, 528, 1141, 578))
    # im1.save('standard/yh.png')


if __name__ == '__main__':
    just_test()
