# encoding: utf-8
"""
@author:  liaoxingyu
@contact: sherlockliao01@gmail.com
"""
import torch
import torch.nn.functional as F
from torch import nn


def normalize(x, axis=-1):
    """Normalizing to unit length along the specified dimension.
    Args:
      x: pytorch Variable
    Returns:
      x: pytorch Variable, same shape as input
    """
    x = 1. * x / (torch.norm(x, 2, axis, keepdim=True).expand_as(x) + 1e-12)
    return x


def normalize_max(x, axis=-1):
    """Normalizing to unit length along the specified dimension.
    Args:
      x: pytorch Variable
    Returns:
      x: pytorch Variable, same shape as input
    """
    dis = torch.sum(x.pow(2), dim=1).sqrt()
    m, _ = torch.max(dis, 0)
    x = x / m
    return x


def euclidean_dist(x, y):
    """
    Args:
      x: pytorch Variable, with shape [m, d]
      y: pytorch Variable, with shape [n, d]
    Returns:
      dist: pytorch Variable, with shape [m, n]
    """
    m, n = x.size(0), y.size(0)
    xx = torch.pow(x, 2).sum(1, keepdim=True).expand(m, n)
    yy = torch.pow(y, 2).sum(1, keepdim=True).expand(n, m).t()
    dist = xx + yy
    dist.addmm_(1, -2, x, y.t())
    dist = dist.clamp(min=1e-12).sqrt()  # for numerical stability
    return dist


def hard_example_mining(dist_mat, labels, return_inds=False):
    """For each anchor, find the hardest positive and negative sample.
    Args:
      dist_mat: pytorch Variable, pair wise distance between samples, shape [N, N]
      labels: pytorch LongTensor, with shape [N]
      return_inds: whether to return the indices. Save time if `False`(?)
    Returns:
      dist_ap: pytorch Variable, distance(anchor, positive); shape [N]
      dist_an: pytorch Variable, distance(anchor, negative); shape [N]
      p_inds: pytorch LongTensor, with shape [N];
        indices of selected hard positive samples; 0 <= p_inds[i] <= N - 1
      n_inds: pytorch LongTensor, with shape [N];
        indices of selected hard negative samples; 0 <= n_inds[i] <= N - 1
    NOTE: Only consider the case in which all labels have same num of samples,
      thus we can cope with all anchors in parallel.
    """

    assert len(dist_mat.size()) == 2
    assert dist_mat.size(0) == dist_mat.size(1)
    N = dist_mat.size(0)

    # shape [N, N]
    is_pos = labels.expand(N, N).eq(labels.expand(N, N).t())
    is_neg = labels.expand(N, N).ne(labels.expand(N, N).t())

    # `dist_ap` means distance(anchor, positive)
    # both `dist_ap` and `relative_p_inds` with shape [N, 1]
    dist_ap, relative_p_inds = torch.max(
        dist_mat[is_pos].contiguous().view(N, -1), 1, keepdim=True)
    # `dist_an` means distance(anchor, negative)
    # both `dist_an` and `relative_n_inds` with shape [N, 1]
    dist_an, relative_n_inds = torch.min(
        dist_mat[is_neg].contiguous().view(N, -1), 1, keepdim=True)
    dist_an_mean = torch.mean(dist_mat[is_neg].contiguous().view(N, -1), dim=1)
    # shape [N]
    dist_ap = dist_ap.squeeze(1)
    dist_an = dist_an.squeeze(1)

    if return_inds:
        # shape [N, N]
        ind = (labels.new().resize_as_(labels)
               .copy_(torch.arange(0, N).long())
               .unsqueeze(0).expand(N, N))
        # shape [N, 1]
        p_inds = torch.gather(
            ind[is_pos].contiguous().view(N, -1), 1, relative_p_inds.data)
        n_inds = torch.gather(
            ind[is_neg].contiguous().view(N, -1), 1, relative_n_inds.data)
        # shape [N]
        p_inds = p_inds.squeeze(1)
        n_inds = n_inds.squeeze(1)
        return dist_ap, dist_an, dist_an_mean, p_inds, n_inds

    return dist_ap, dist_an, dist_an_mean


class TripletAttentionLoss(object):
    """Modified from Tong Xiao's open-reid (https://github.com/Cysu/open-reid).
    Related Triplet Loss theory can be found in paper 'In Defense of the Triplet
    Loss for Person Re-Identification'."""

    def __init__(self, margin=None):
        self.margin = margin
        self.attn_loss = nn.MSELoss()
        if margin is not None:
            self.ranking_loss = nn.MarginRankingLoss(margin=margin)
        else:
            self.ranking_loss = nn.SoftMarginLoss()
        self.weight_param = nn.Parameter(torch.ones(1, dtype=torch.float, requires_grad=True).cuda())

    def __call__(self, global_feat, labels, cls_param, normalize_feature=False):
        if normalize_feature:
            global_feat = normalize_max(global_feat, axis=-1)
        dist_mat = euclidean_dist(global_feat, global_feat)
        dist_ap, dist_an, dist_an_mean, ind_pos, ind_neg = hard_example_mining(
            dist_mat, labels, True)
        neg_weight = self.weight(ind_neg, cls_param.detach(), labels)
        dist_neg = torch.sum((global_feat*neg_weight - global_feat[ind_neg]*neg_weight).pow(2), dim=1).sqrt()
        dist_pos = torch.sum((global_feat*neg_weight - global_feat[ind_pos]*neg_weight).pow(2), dim=1).sqrt()
        y = dist_an.new().resize_as_(dist_an).fill_(1)

        if self.margin is not None:
            loss = self.ranking_loss(dist_an.detach(), dist_ap, y) + self.ranking_loss(dist_an_mean, dist_ap.detach(), y) \
                   + self.ranking_loss(dist_neg, dist_pos, y)        # NEWTH
            # loss = self.ranking_loss(dist_an.detach(), dist_ap, y) + self.ranking_loss(dist_neg, dist_pos, y) # EWTH
            # loss = self.ranking_loss(dist_an.detach(), dist_ap, y) + self.ranking_loss(dist_an_mean, dist_ap.detach(), y) # HNTH
            # loss = self.ranking_loss(dist_an.detach(), dist_ap, y) # HTH
            # loss = self.ranking_loss(dist_an, dist_ap, y) # TH
        else:
            loss = self.ranking_loss(dist_an.detach() - dist_ap, y) + self.ranking_loss(dist_neg - dist_pos, y) \
                   + self.ranking_loss(dist_an_mean, dist_ap.detach(), y)
        return loss, dist_ap, dist_an

    def weight(self, ind_neg, param, target):
        t = 0.1
        weight_neg1 = param[target]
        weight_neg2 = param[target[ind_neg]]
        weight_neg = torch.abs(weight_neg1-weight_neg2)
        max, _ = torch.max(weight_neg, dim=1, keepdim=True)
        weight_neg = weight_neg / (max + 1e-12)
        weight_neg[weight_neg < t] = -self.weight_param
        weight_neg = weight_neg + self.weight_param

        return weight_neg


class CrossEntropyLabelSmooth(nn.Module):
    """Cross entropy loss with label smoothing regularizer.

    Reference:
    Szegedy et al. Rethinking the Inception Architecture for Computer Vision. CVPR 2016.
    Equation: y = (1 - epsilon) * y + epsilon / K.

    Args:
        num_classes (int): number of classes.
        epsilon (float): weight.
    """
    def __init__(self, num_classes, epsilon=0.1, use_gpu=True):
        super(CrossEntropyLabelSmooth, self).__init__()
        self.num_classes = num_classes
        self.epsilon = epsilon
        self.use_gpu = use_gpu
        self.logsoftmax = nn.LogSoftmax(dim=1)

    def forward(self, inputs, targets):
        """
        Args:
            inputs: prediction matrix (before softmax) with shape (batch_size, num_classes)
            targets: ground truth labels with shape (num_classes)
        """
        log_probs = self.logsoftmax(inputs)
        targets = torch.zeros(log_probs.size()).scatter_(1, targets.unsqueeze(1).data.cpu(), 1)
        if self.use_gpu: targets = targets.cuda()
        targets = (1 - self.epsilon) * targets + self.epsilon / self.num_classes
        loss = (- targets * log_probs).mean(0).sum()
        return loss
