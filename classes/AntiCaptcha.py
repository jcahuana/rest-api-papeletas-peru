import os
from anticaptchaofficial.imagecaptcha import *


class Captcha:
    # token = os.environ("ANTICAPTCHA_TOKEN")
    token = os.environ.get("ANTICAPTCHA_TOKEN")
    # token = open('./private/token.txt').readline().strip()

    def __init__(self, captcha_image_path):
        print("init")
        self.captcha_image_path = captcha_image_path

    # code
    def getCode(self):
        solver = imagecaptcha()
        solver.set_verbose(1)
        solver.set_key(self.token)
        captachResult = solver.solve_and_return_solution(
            self.captcha_image_path)
        return captachResult
