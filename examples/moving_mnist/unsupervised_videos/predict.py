#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Yuki Furuta <furushchev@jsk.imi.i.u-tokyo.ac.jp>

import click
import os.path as osp
import sys
import chainervr
import chainervr.utils.predict as P


@click.group()
def cli():
    pass


@cli.command()
@click.argument("model_path")
@P.predict_params
@click.option("--disable-predict", is_flag=True)
@click.option("--layers-num", type=int, default=2)
@click.option("--start-from", type=int, default=0)
@click.option("--images-num", type=int, default=100)
def predict(model_path, gpu, out, split, disable_predict, layers_num,
            in_episodes, out_episodes, start_from, images_num):

    P.info("Loading model from %s" % model_path)

    model = chainervr.models.RPLSTM(
        n_channels=1, patch_size=(64, 64),
        n_layers=layers_num, predict=not disable_predict,
        in_episodes=in_episodes, out_episodes=out_episodes)

    model.reset_state()

    P.info("Loading dataset")

    dataset = chainervr.datasets.MovingMnistDataset(
        split=split, channels_num=1)

    P.predict(
        model=model,
        model_path=model_path,
        dataset=dataset,
        gpu=gpu, out=out,
        in_episodes=in_episodes,
        out_episodes=out_episodes,
        start_from=start_from,
        images_num=images_num)


@cli.command()
@click.argument("model_dir")
@P.predict_params
@click.option("--disable-predict", is_flag=True)
@click.option("--layers-num", type=int, default=2)
@click.option("--image-num", type=int, default=0)
@click.option("--skip-num", type=int, default=1)
def summary(model_dir, gpu, out, split, disable_predict, layers_num,
            in_episodes, out_episodes, image_num, skip_num):
    model = chainervr.models.RPLSTM(
        n_channels=1, patch_size=(64, 64),
        n_layers=layers_num, predict=not disable_predict,
        in_episodes=in_episodes, out_episodes=out_episodes)

    model.reset_state()

    P.info("Loading dataset")

    dataset = chainervr.datasets.MovingMnistDataset(
        split=split, channels_num=1)

    P.predict_summary(
        model=model,
        model_dir=model_dir,
        dataset=dataset,
        gpu=gpu,
        in_episodes=in_episodes,
        out_episodes=out_episodes,
        out=out,
        image_num=image_num,
        skip_num=skip_num)


if __name__ == '__main__':
    cli()
