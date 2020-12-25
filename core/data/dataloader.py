from torch.utils.data import DataLoader
from torchvision import transforms

from core.data.dataset import FewShotDataset
from .collates import *


MEAN = [120.39586422 / 255.0, 115.59361427 / 255.0, 104.54012653 / 255.0]
STD = [70.68188272 / 255.0, 68.27635443 / 255.0, 72.54505529 / 255.0]

CJ_DICT = {'brightness': 0.4, 'contrast': 0.4, 'saturation': 0.4}


def get_dataloader(config, mode='train'):
    """

    :param config:
    :param mode:
    :return:
    """
    trfms_list = []
    if mode == 'train' and config['augment']:
        if config['image_size'] == 224:
            trfms_list.append(transforms.Resize((256, 256)))
            trfms_list.append(transforms.RandomCrop((224, 224)))
        elif config['image_size'] == 84:
            trfms_list.append(transforms.Resize((92, 92)))
            trfms_list.append(transforms.RandomCrop((84, 84)))
        else:
            raise RuntimeError

        trfms_list.append(transforms.ColorJitter(**CJ_DICT))
        trfms_list.append(transforms.RandomHorizontalFlip())
    else:
        if config['image_size'] == 224:
            trfms_list.append(transforms.Resize((224, 224)))
        elif config['image_size'] == 84:
            trfms_list.append(transforms.Resize((84, 84)))
        else:
            raise RuntimeError

    trfms_list.append(transforms.ToTensor())
    trfms_list.append(transforms.Normalize(mean=MEAN, std=STD))
    trfms = transforms.Compose(trfms_list)

    dataset = FewShotDataset(data_root=config['data_root'], mode=mode,
                             way_num=config['way_num'],
                             shot_num=config['shot_num'],
                             query_num=config['query_num'],
                             episode_num=config['train_episode']
                             if mode == 'train' else config['test_episode'], )

    collate_fn = get_collate_fn(config, trfms)
    # collate_fn = None
    dataloader = DataLoader(
            dataset, batch_size=1, shuffle=True,
            num_workers=config['n_gpu'] * 4, drop_last=True, collate_fn=collate_fn, pin_memory=True)

    return dataloader
