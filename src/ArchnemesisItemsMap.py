from typing import List
from PIL import ImageTk, Image
import cv2
import numpy as np

from DataClasses import RecipeItemNode


class ArchnemesisItemsMap:
    """
    Holds the information about all archnemesis items, recipes, images and map them together
    """
    def __init__(self, scale: float):
        # Put everything into the list so we could maintain the display order
        self._arch_items = [
            ('奇塔弗之触', ['图克哈玛之触', '艾贝拉斯之触', '腐化', '灵枢炸弹']),
            ('纯净之触', ['月影之触', '日耀之触', '镜影', '魔力虹吸']),
            ('沙卡丽之触', ['纠缠', '噬魂者', '干旱使者']),
            ('艾贝拉斯之触', ['火击者', '疯狂', '回春']),
            ('图克哈玛之触', ['碎骨者', '刽子手', '岩浆屏障']),
            ('惊海王之触', ['冰牢', '风击者', '捷化召唤生物']),
            ('阿拉卡力之触', ['灵枢炸弹', '纠缠', '暗影大师']),
            ('日耀之触', ['无懈可击', '岩浆屏障', '强化召唤生物']),
            ('月影之触', ['无懈可击', '霜击者', '强化召唤生物']),
            ('雕像', ['魔蛊', '恶语术', '腐化']),
            ('强化元素', ['召唤师', '钢注', '混沌编织者']),
            ('剥皮水晶', ['恒久冻土', '回春', '狂战士']),
            ('无懈可击', ['哨兵', '勇士', '圣职']),
            ('腐化', ['放血者', '混沌编织者']),
            ('魔力虹吸', ['圣职', '蓄电']),
            ('风击者', ['风暴编织者', '迅捷']),
            ('镜影', ['回音人', '造灵体']),
            ('岩浆屏障', ['烈火焚烧', '碎骨者']),
            ('召唤师', ['火焰编织者', '冰霜编织者', '风暴编织者']),
            ('灵枢炸弹', ['死灵法师', '烈火焚烧']),
            ('火击者', ['火焰编织者', '迅捷']),
            ('噬魂者', ['造灵体', '死灵法师', '巨像']),
            ('冰牢', ['恒久冻土', '哨兵']),
            ('霜击者', ['冰霜编织者', '迅捷']),
            ('树人部落', ['毒', '哨兵', '钢注']),
            ('时间泡泡', ['勇士', '魔蛊', '奥术增幅者']),
            ('纠缠', ['毒', '放血者']),
            ('干旱使者', ['恶语术', '死眼']),
            ('魔蛊', ['混沌编织者', '回音人']),
            ('刽子手', ['疯狂', '狂战士']),
            ('回春', ['巨像', '吸血鬼']),
            ('死灵法师', ['投弹手', '超载']),
            ('诈欺师', ['超载', '暗影大师', '回音人']),
            ('暗影大师', ['死眼', '吸血鬼']),
            ('强化召唤生物', ['死灵法师', '刽子手', '巨像']),
            ('捷化召唤生物', ['蓄电', '奥术增幅者']),
            ('奥术增幅者', []),
            ('狂战士', []),
            ('放血者', []),
            ('投弹手', []),
            ('碎骨者', []),
            ('混沌编织者', []),
            ('圣职', []),
            ('死眼', []),
            ('蓄电', []),
            ('回音人', []),
            ('火焰编织者', []),
            ('疯狂', []),
            ('冰霜编织者', []),
            ('巨像', []),
            ('迅捷', []),
            ('烈火焚烧', []),
            ('勇士', []),
            ('恶语术', []),
            ('丰富', []),
            ('超载', []),
            ('恒久冻土', []),
            ('哨兵', []),
            ('造灵体', []),
            ('钢注', []),
            ('风暴编织者', []),
            ('毒', []),
            ('吸血鬼', []),
            ('不需要', [])
        ]
        self._images = dict()
        self._small_image_size = 30
        self._update_images(scale)

    def _update_images(self, scale):
        self._scale = scale
        for item, _ in self._arch_items:
            self._images[item] = dict()
            image = self._load_image(item, scale)
            self._image_size = image.size
            self._images[item]['scan-image'] = self._create_scan_image(image)
            # Convert the image to Tk image because we're going to display it
            self._images[item]['display-image'] = ImageTk.PhotoImage(image=image)
            image = image.resize((self._small_image_size, self._small_image_size))
            self._images[item]['display-small-image'] = ImageTk.PhotoImage(image=image)

    def _load_image(self, item: str, scale: float):
        image = Image.open(f'pictures/{item}.png')
        # Scale the image according to the input parameter
        return image.resize((int(image.width * scale), int(image.height * scale)))

    def _create_scan_image(self, image):
        # Remove alpha channel and replace it with predefined background color
        background = Image.new('RGBA', image.size, (10, 10, 32))
        image_without_alpha = Image.alpha_composite(background, image)
        scan_template = cv2.cvtColor(np.array(image_without_alpha), cv2.COLOR_RGB2BGR)
        w, h, _ = scan_template.shape

        # Crop the image to help with scanning
        return scan_template[int(h * 0.16):int(h * 0.75), int(w * 0.16):int(w * 0.85)]


    def get_scan_image(self, item):
        return self._images[item]['scan-image']

    def get_display_image(self, item):
        return self._images[item]['display-image']

    def get_display_small_image(self, item):
        return self._images[item]['display-small-image']

    def items(self):
        for item, _ in self._arch_items:
            yield item

    def recipes(self):
        for item, recipe in self._arch_items:
            if recipe:
                yield (item, recipe)

    def get_subtree_for(self, item: str):
        tree = RecipeItemNode(item, [])
        nodes = [tree]
        while len(nodes) > 0:
            node = nodes.pop(0)
            children = self.get_components_for(node.item)
            if len(children) > 0:
                node.components = [RecipeItemNode(c, []) for c in children]
                nodes.extend(node.components)
        return tree

    def get_parent_recipes_for(self, item: str) -> List[str]:
        parents = list()
        for parent, components in self._arch_items:
            if item in components:
                parents.append(parent)
        return parents

    def get_components_for(self, item) -> List[str]:
        return next(l for x, l in self._arch_items if x == item)

    @property
    def image_size(self):
        return self._image_size

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, scale: float) -> None:
        self._update_images(scale)

    @property
    def small_image_size(self):
        return self._small_image_size
