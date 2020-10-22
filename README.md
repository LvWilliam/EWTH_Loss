# The Dilemma of TriHard Loss and an Element-Weighted TriHard Loss for Person Re-Identification

All the proposed losses in this paper are implemented on [Bag of Tricks and A Strong Baseline for Deep Person Re-identification (BoT)](https://github.com/michuanhaohao/reid-strong-baseline) and [Deep Learning for Person Re-identification: A Survey and Outlook (AGW)](https://github.com/mangye16/ReID-Survey).


## Requirements
See [README of BoT](https://github.com/michuanhaohao/reid-strong-baseline/blob/master/README.md) and [README of AGW](https://github.com/mangye16/ReID-Survey/blob/master/README.md) for requirements.


## Training

The models in this paper are trained on BoT and AGW with ResNet50 as the backbone. But a few modifications are needed to make to the baselines.
### Bag of Tricks (BoT)
All the experiments are conducted without center loss, which is optional in BoT.
All the required files are in folder `BoT`.

To train the network with losses in this paper, replace
`baseline.py` in `reid-strong-baseline/modeling/` with `baseline.py`
`trainer.py` in `reid-strong-baseline/engine/` with `trainer.py`
`__init__.py` and `triplet_loss.py` in `reid-strong-baseline/layers/` with `__init__.py` and `triplet_loss.py`.

You can train the network with different losses proposed in this paper, which can be changes in `triplet_loss.py`. The default loss is HNEWTH in `triplet_loss.py`.
Margins in EWTH loss can be changed in `reid-strong-baseline/configs/softmax_triplet.yml` and `triplet_loss.py`.
The hyper parameter $t$ can be changed in `triplet_loss.py`.
Other settings of BoT are default and other informations of training are available in `reid-strong-baseline/README.md`.

### AGW
All the required files are in folder `AGW`.

To train the network with losses in this paper, turn WEIGHT_REGULARIZED_TRIPLET into "off" in  `ReID-Survey/configs/AGW_baseline.yml` and replace
`triplet_loss.py` in `ReID-Survey/modeling/layer/` with `triplet_loss.py`
`baseline.py` in `ReID-Survey/modeling/` with `baseline.py`.

You can train the network with different losses proposed in this paper, which can be changes in `triplet_loss.py`. The default loss is HNEWTH in `triplet_loss.py`.
Margins in EWTH loss can be changed in `ReID-Survey/config/defaults.py` and `triplet_loss.py`.
The hyper parameter $t$ can be changed in `triplet_loss.py`.
Other settings of AGW are default and other informations of training are available in `ReID-Survey/README.md`.

## Evaluation

See [README of BoT](https://github.com/michuanhaohao/reid-strong-baseline/blob/master/README.md) and [README of AGW](https://github.com/mangye16/ReID-Survey/blob/master/README.md).

## Pre-trained Models
The pre-trained ResNet50 model will be downloaded to the specified locations in  BoT and AGW. See [README of BoT](https://github.com/michuanhaohao/reid-strong-baseline/blob/master/README.md) and [README of AGW](https://github.com/mangye16/ReID-Survey/blob/master/README.md) for further informations.

## Results
In AGW+HNTH, $\alpha_1=0.1$ and in AGW+EWTH, $\alpha_2=0.2$.
All the other margins are default values 0.3.
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-c3ow" rowspan="2">Method</th>
    <th class="tg-c3ow" colspan="2">Market1501</th>
    <th class="tg-c3ow" colspan="2">MSMT17</th>
    <th class="tg-c3ow" rowspan="2">Method</th>
    <th class="tg-c3ow" colspan="2">Market1501</th>
    <th class="tg-c3ow" colspan="2">MSMT17</th>
  </tr>
  <tr>
    <td class="tg-c3ow">mAP</td>
    <td class="tg-c3ow">rank-1</td>
    <td class="tg-c3ow">mAP</td>
    <td class="tg-c3ow">rank-1</td>
    <td class="tg-c3ow">mAP</td>
    <td class="tg-c3ow">rank-1</td>
    <td class="tg-c3ow">mAP</td>
    <td class="tg-c3ow">rank-1</td>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-c3ow">BoT+TH</td>
    <td class="tg-c3ow">85.6%</td>
    <td class="tg-c3ow">94.1%</td>
    <td class="tg-c3ow">45.1%</td>
    <td class="tg-c3ow">63.9%</td>
    <td class="tg-c3ow">AGW+TH</td>
    <td class="tg-c3ow">87.7%</td>
    <td class="tg-c3ow">95.0%</td>
    <td class="tg-c3ow">48.4%</td>
    <td class="tg-c3ow">67.9%</td>
  </tr>
  <tr>
    <td class="tg-c3ow">BoT+HTH</td>
    <td class="tg-c3ow">86.6%</td>
    <td class="tg-c3ow">94.6%</td>
    <td class="tg-c3ow">45.0%</td>
    <td class="tg-c3ow">63.9%</td>
    <td class="tg-c3ow">AGW+HTH</td>
    <td class="tg-c3ow">88.1%</td>
    <td class="tg-c3ow">95.4%</td>
    <td class="tg-c3ow">48.1%</td>
    <td class="tg-c3ow">67.6%</td>
  </tr>
  <tr>
    <td class="tg-c3ow">BoT+EWTH</td>
    <td class="tg-c3ow">87.7%</td>
    <td class="tg-c3ow">95.0%</td>
    <td class="tg-c3ow">48.7%</td>
    <td class="tg-c3ow">67.8%</td>
    <td class="tg-c3ow">AGW+EWTH</td>
    <td class="tg-c3ow">88.5%</td>
    <td class="tg-c3ow">95.4%</td>
    <td class="tg-c3ow">50.4%</td>
    <td class="tg-c3ow">69.6%</td>
  </tr>
  <tr>
    <td class="tg-c3ow">BoT+NEWTH</td>
    <td class="tg-c3ow">88.4%</td>
    <td class="tg-c3ow">95.1%</td>
    <td class="tg-c3ow">49.7%</td>
    <td class="tg-c3ow">68.1%</td>
    <td class="tg-c3ow">AGW+NEWTH</td>
    <td class="tg-c3ow">89.4%</td>
    <td class="tg-c3ow">95.6%</td>
    <td class="tg-c3ow">53.1%</td>
    <td class="tg-c3ow">71.5%</td>
  </tr>
  <tr>
    <td class="tg-c3ow">BoT+TH+FN</td>
    <td class="tg-c3ow">86.3%</td>
    <td class="tg-c3ow">94.1%</td>
    <td class="tg-c3ow">45.2%</td>
    <td class="tg-c3ow">63.8%</td>
    <td class="tg-c3ow">AGW+TH+FN</td>
    <td class="tg-c3ow">88.0%</td>
    <td class="tg-c3ow">95.1%</td>
    <td class="tg-c3ow">47.7%</td>
    <td class="tg-c3ow">66.3%</td>
  </tr>
</tbody>
</table>
