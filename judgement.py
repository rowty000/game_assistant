# -*- coding: utf-8 -*-
# @Time : 2019/4/11 10:23
# @Author : Vanya
import math
from PIL import Image, ImageChops
import aircv as ac
import cv2


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
        return self.is_same(im, im2, 300)

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

    def is_exploration_in_page(self, pic):
        im = Image.open(pic)
        im = im.convert('L')
        im = im.crop((1030, 580, 1130, 630))
        im2 = Image.open('standard/exploration_entry.png')
        return self.is_same(im, im2, 300)

    @ staticmethod
    def get_attack_pos(pic, all_pos=False, pic_as_img=False):
        im = pic if pic_as_img else ac.imread(pic)
        im2 = ac.imread('standard/attack.png')
        if all_pos:
            match_result = ac.find_all_template(im, im2, 0.95, 6)
            if match_result:
                return [x['result'] for x in match_result]
        else:
            match_result = ac.find_template(im, im2, 0.95)
            if match_result:
                return match_result['result']

    @staticmethod
    def get_crop_pic(pic, box):
        im = ac.imread(pic)
        return im[int(box[1]):int(box[3]), int(box[0]):int(box[2])]

    @ staticmethod
    def get_attack_boss_pos(pic):
        im = ac.imread(pic)
        im2 = ac.imread('standard/attack_boss.png')
        match_result = ac.find_template(im, im2, 0.95)
        if match_result:
            return match_result['result']

    @staticmethod
    def get_boss_box_pos(pic):
        im = ac.imread(pic)
        im2 = ac.imread('standard/box.png')
        match_result = ac.find_template(im, im2, 0.95)
        if match_result:
            return match_result['result']

    @staticmethod
    def get_experience_pos(pic):
        im = ac.imread(pic)
        im2 = ac.imread('standard/experience.png')
        match_result = ac.find_sift(im, im2)
        if match_result:
            if match_result['confidence'][1] > 15:
                return match_result['result']

    def is_quit_ok_page(self, pic):
        im = Image.open(pic)
        im = im.convert('L')
        im = im.crop((800, 430, 900, 470))
        im2 = Image.open('standard/quit_ok.png')
        return self.is_same(im, im2, 300)

    def is_quit_page(self, pic):
        im = Image.open(pic)
        im = im.convert('L')
        im = im.crop((30, 50, 80, 90))
        im2 = Image.open('standard/quit.png')
        return self.is_same(im, im2, 300)


def just_test():
    # im = Image.open('pics/tansuo1.png')
    # im = im.convert('L')
    # im1 = im.crop((30, 50, 80, 90))
    # im1.save('standard/ttt.png')

    # im = ac.imread('pics/tansuo14.png')
    # im2 = ac.imread('standard/experience.png')
    # # match_result = ac.find_template(im, im2, 0.95)
    # match_result = ac.find_sift(im, im2)
    # print(match_result)

    judge = Judgement()
    # im = judge.get_crop_pic('pics/tansuo14.png', (100, 100, 300, 600))
    # cv2.imshow('tt', im)
    # cv2.waitKey()
    print(judge.is_quit_ok_page('pics/tansuo15.png'))
    # pos = judge.get_attack_pos('auto_challenge.png')
    # if pos:
    #     print(pos)


if __name__ == '__main__':
    just_test()
