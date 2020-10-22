# EWTH_Loss
The implementation of the NeurIPS2020 paper: The Dilemma of TriHard Loss and an Element-Weighted TriHard Loss for Person Re-Identification
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
In AGW+HNTH, $\phi=0.1$ and in AGW+EWTH, $\alpha=0.2$.
All the other margins are default values 0.3.
  <tr>
    <th class="tg-c3ow" rowspan="2">Method</th>
    <th class="tg-c3ow" colspan="2">Market1501</th>
    <th class="tg-c3ow" colspan="2">DukeMTMC-reID</th>
    <th class="tg-c3ow" rowspan="2">Method</th>
    <th class="tg-c3ow" colspan="2">Market1501</th>
    <th class="tg-c3ow" colspan="2">DukeMTMC-ReID</th>
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
    <td class="tg-c3ow">85.60%</td>
    <td class="tg-c3ow">94.10%</td>
    <td class="tg-c3ow">75.80%</td>
    <td class="tg-c3ow">86.10%</td>
    <td class="tg-c3ow">BoT+HNEWTH</td>
    <td class="tg-c3ow">86.70%</td>
    <td class="tg-c3ow">94.90%</td>
    <td class="tg-c3ow">76.50%</td>
    <td class="tg-c3ow">86.80%</td>
  </tr>
  <tr>
    <td class="tg-c3ow">BoT+TH+FN</td>
    <td class="tg-c3ow">86.30%</td>
    <td class="tg-c3ow">94.10%</td>
    <td class="tg-c3ow">76.70%</td>
    <td class="tg-c3ow">86.80%</td>
    <td class="tg-c3ow">BoT+NEWTH</td>
    <td class="tg-c3ow">86.90%</td>
    <td class="tg-c3ow">94.60%</td>
    <td class="tg-c3ow">76.80%</td>
    <td class="tg-c3ow">87.40%</td>
  </tr>
  <tr>
    <td class="tg-c3ow">BoT+HTH</td>
    <td class="tg-c3ow">86.60%</td>
    <td class="tg-c3ow">94.60%</td>
    <td class="tg-c3ow">77.10%</td>
    <td class="tg-c3ow">87.70%</td>
    <td class="tg-c3ow">BoT+HEWTH</td>
    <td class="tg-c3ow">87.70%</td>
    <td class="tg-c3ow">95.00%</td>
    <td class="tg-c3ow">77.80%</td>
    <td class="tg-c3ow">88.40%</td>
  </tr>
  <tr>
    <td class="tg-c3ow">BoT+HNTH</td>
    <td class="tg-c3ow">87.30%</td>
    <td class="tg-c3ow">94.90%</td>
    <td class="tg-c3ow">77.80%</td>
    <td class="tg-c3ow">87.60%</td>
    <td class="tg-c3ow">BoT+HNEWTH</td>
    <td class="tg-c3ow">88.40%</td>
    <td class="tg-c3ow">95.10%</td>
    <td class="tg-c3ow">78.80%</td>
    <td class="tg-c3ow">88.60%</td>
  </tr>
  <tr>
    <td class="tg-c3ow">AGW+TH</td>
    <td class="tg-c3ow">87.70%</td>
    <td class="tg-c3ow">95.00%</td>
    <td class="tg-c3ow">78.20%</td>
    <td class="tg-c3ow">88.30%</td>
    <td class="tg-c3ow">AGW+EWTH</td>
    <td class="tg-c3ow">87.70%</td>
    <td class="tg-c3ow">95.30%</td>
    <td class="tg-c3ow">78.50%</td>
    <td class="tg-c3ow">88.70%</td>
  </tr>
  <tr>
    <td class="tg-c3ow">AGW+TH+FN</td>
    <td class="tg-c3ow">88.00%</td>
    <td class="tg-c3ow">95.10%</td>
    <td class="tg-c3ow">78.60%</td>
    <td class="tg-c3ow">88.60%</td>
    <td class="tg-c3ow">AGW+NEWTH</td>
    <td class="tg-c3ow">87.70%</td>
    <td class="tg-c3ow">95.00%</td>
    <td class="tg-c3ow">78.50%</td>
    <td class="tg-c3ow">88.40%</td>
  </tr>
  <tr>
    <td class="tg-c3ow">AGW+HTH</td>
    <td class="tg-c3ow">88.10%</td>
    <td class="tg-c3ow">95.40%</td>
    <td class="tg-c3ow">78.50%</td>
    <td class="tg-c3ow">88.30%</td>
    <td class="tg-c3ow">AGW+HEWTH</td>
    <td class="tg-c3ow">88.50%</td>
    <td class="tg-c3ow">95.40%</td>
    <td class="tg-c3ow">78.90%</td>
    <td class="tg-c3ow">89.70%</td>
  </tr>
  <tr>
    <td class="tg-c3ow">AGW+HNTH</td>
    <td class="tg-c3ow">88.10%</td>
    <td class="tg-c3ow">95.60%</td>
    <td class="tg-c3ow">79.70%</td>
    <td class="tg-c3ow">89.30%</td>
    <td class="tg-c3ow">AGW+HNEWTH</td>
    <td class="tg-c3ow">89.40%</td>
    <td class="tg-c3ow">95.60%</td>
    <td class="tg-c3ow">80.50%</td>
    <td class="tg-c3ow">90.50%</td>
  </tr>
</tbody>
</table>
