---
layout: post
title: Attention Is All You Need · 注意力就是你所需要的一切
date: 2026-09-15
categories: 技术
description: Transformer 原论文的中英对照全译。英文原文以引用块呈现，中文逐段对应；含原论文全部 6 张插图与表格，公式沿用原文的纯文本排法。
---


**中英文对照版 / English–Chinese Bilingual Edition**

| 项目 | 内容 |
| --- | --- |
| 原始文件 | `注意力.pdf`（工作区根目录） |
| 论文出处 | 31st Conference on Neural Information Processing Systems (NIPS 2017), Long Beach, CA, USA. |
| arXiv 版本 | arXiv:1706.03762v7 [cs.CL] 2 Aug 2023 |
| 作者 | Ashish Vaswani、Noam Shazeer、Niki Parmar、Jakob Uszkoreit、Llion Jones、Aidan N. Gomez、Łukasz Kaiser、Illia Polosukhin |
| 插图目录 | `/assets/attention/`（自原 PDF 导出） |

## 体例说明 / Conventions

- **英文原文以引用块（`>`）标示，紧随其后的中文段落为其对应译文。** 原文与译文段落一一对应，便于逐段对照。
- 公式采用 Unicode 纯文本排版，以便在任何 Markdown 阅读器中正常显示：下标写作 `d_k`，上标写作 `QK^T`，开方写作 `√d_k`。公式编号沿用原文编号 (1)–(3)。
- 表格保留原数据不变，表头采用中英双语；原表中未列出的空白单元格同样保留为空白。
- 图注中英对照；插图从原 PDF 中导出并嵌入本文档。
- 参考文献按学术惯例保留英文原貌，不作逐条翻译；文末另附**术语对照表**供检索。
- 原文脚注按原文编号以上标数字（如 ⁴、⁵）标记，紧随相应段落，同样中英对照。

---

## 版权声明 / Permission Notice

> Provided proper attribution is provided, Google hereby grants permission to reproduce the tables and figures in this paper solely for use in journalistic or scholarly works.

在给予适当署名的前提下，Google 特此授予许可，允许仅为新闻报道或学术研究之目的复制本论文中的表格与插图。

---

## 标题与作者 / Title and Authors

> **Attention Is All You Need**

**注意力就是你所需要的一切**

> Ashish Vaswani\* — Google Brain — avaswani@google.com
> Noam Shazeer\* — Google Brain — noam@google.com
> Niki Parmar\* — Google Research — nikip@google.com
> Jakob Uszkoreit\* — Google Research — usz@google.com
> Llion Jones\* — Google Research — llion@google.com
> Aidan N. Gomez\*† — University of Toronto — aidan@cs.toronto.edu
> Łukasz Kaiser\* — Google Brain — lukaszkaiser@google.com
> Illia Polosukhin\*‡ — illia.polosukhin@gmail.com

Ashish Vaswani\*（谷歌大脑，avaswani@google.com）、Noam Shazeer\*（谷歌大脑，noam@google.com）、Niki Parmar\*（谷歌研究院，nikip@google.com）、Jakob Uszkoreit\*（谷歌研究院，usz@google.com）、Llion Jones\*（谷歌研究院，llion@google.com）、Aidan N. Gomez\*†（多伦多大学，aidan@cs.toronto.edu）、Łukasz Kaiser\*（谷歌大脑，lukaszkaiser@google.com）、Illia Polosukhin\*‡（illia.polosukhin@gmail.com）

（人名、邮箱与机构名按原文保留，机构名附中文对照：Google Brain 谷歌大脑，Google Research 谷歌研究院，University of Toronto 多伦多大学。）

---

## 摘要 / Abstract

> The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

主流的序列转导模型基于复杂的循环或卷积神经网络，其中包含一个编码器和一个解码器。性能最好的模型还通过注意力机制连接编码器与解码器。我们提出了一种新的、简单的网络架构——**Transformer**，它完全基于注意力机制，彻底摒弃了循环与卷积。在两个机器翻译任务上的实验表明，这些模型在质量上更优，同时更易于并行化，训练所需时间也显著减少。我们的模型在 WMT 2014 英德翻译任务上取得 28.4 BLEU，比现有最佳结果（包括集成模型）提升超过 2 BLEU。在 WMT 2014 英法翻译任务上，我们的模型在 8 块 GPU 上训练 3.5 天后，建立了 41.8 的单模型最新最佳 BLEU 分数，其训练成本仅为文献中最佳模型的一小部分。我们还证明，Transformer 能很好地泛化到其他任务：将其成功应用于英语成分句法分析，无论训练数据规模较大还是有限，均表现良好。

---

## 作者贡献脚注 / Author Footnotes

> \*Equal contribution. Listing order is random. Jakob proposed replacing RNNs with self-attention and started the effort to evaluate this idea. Ashish, with Illia, designed and implemented the first Transformer models and has been crucially involved in every aspect of this work. Noam proposed scaled dot-product attention, multi-head attention and the parameter-free position representation and became the other person involved in nearly every detail. Niki designed, implemented, tuned and evaluated countless model variants in our original codebase and tensor2tensor. Llion also experimented with novel model variants, was responsible for our initial codebase, and efficient inference and visualizations. Lukasz and Aidan spent countless long days designing various parts of and implementing tensor2tensor, replacing our earlier codebase, greatly improving results and massively accelerating our research.

\* 贡献相同。作者排序为随机顺序。Jakob 提出用自注意力替代 RNN，并启动了评估这一想法的研究工作。Ashish 与 Illia 设计并实现了最早的 Transformer 模型，并在本工作的各个方面都起到了关键作用。Noam 提出了缩放点积注意力、多头注意力以及无参数的位置表示，并成为几乎参与每一个细节的另一位作者。Niki 在我们最初的代码库和 tensor2tensor 中设计、实现、调优并评估了无数模型变体。Llion 也试验了新颖的模型变体，负责我们最初的代码库，以及高效推理与可视化工作。Lukasz 和 Aidan 花费了无数漫长的日夜，设计并实现 tensor2tensor 的各个部分，用它替换了我们早先的代码库，大幅改善了结果并极大地加速了我们的研究。

> †Work performed while at Google Brain.

† 本工作于作者在谷歌大脑（Google Brain）任职期间完成。

> ‡Work performed while at Google Research.

‡ 本工作于作者在谷歌研究院（Google Research）任职期间完成。

> 31st Conference on Neural Information Processing Systems (NIPS 2017), Long Beach, CA, USA.
> arXiv:1706.03762v7 [cs.CL] 2 Aug 2023

第 31 届神经信息处理系统大会（NIPS 2017），美国加州长滩。
arXiv:1706.03762v7 [cs.CL]，2023 年 8 月 2 日。

---

## 1 引言 / Introduction

> Recurrent neural networks, long short-term memory [13] and gated recurrent [7] neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling and machine translation [35, 2, 5]. Numerous efforts have since continued to push the boundaries of recurrent language models and encoder-decoder architectures [38, 24, 15].

循环神经网络，尤其是长短期记忆网络 [13] 和门控循环神经网络 [7]，已被牢固确立为序列建模与转导问题（如语言建模和机器翻译）中的最先进方法 [35, 2, 5]。此后，大量研究工作持续拓展着循环语言模型与编码器-解码器架构的边界 [38, 24, 15]。

> Recurrent models typically factor computation along the symbol positions of the input and output sequences. Aligning the positions to steps in computation time, they generate a sequence of hidden states h_t, as a function of the previous hidden state h_{t−1} and the input for position t. This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths, as memory constraints limit batching across examples. Recent work has achieved significant improvements in computational efficiency through factorization tricks [21] and conditional computation [32], while also improving model performance in case of the latter. The fundamental constraint of sequential computation, however, remains.

循环模型通常沿输入和输出序列的符号位置来分解计算。将位置与计算时间步对齐后，它们生成隐状态序列 h_t，其取决于前一隐状态 h_{t−1} 以及位置 t 处的输入。这种内在的序列性排除了训练样本内部的并行化；而在序列较长时这一点变得尤为关键，因为内存限制会制约跨样本的批处理。近期工作通过分解技巧 [21] 和条件计算 [32] 在计算效率上取得了显著改进，后者还同时提升了模型性能。然而，顺序计算这一根本性约束依然存在。

> Attention mechanisms have become an integral part of compelling sequence modeling and transduction models in various tasks, allowing modeling of dependencies without regard to their distance in the input or output sequences [2, 19]. In all but a few cases [27], however, such attention mechanisms are used in conjunction with a recurrent network.

在各类任务中，注意力机制已成为出色的序列建模与转导模型不可或缺的组成部分，它使模型能够对依赖关系建模，而不必考虑这些依赖在输入或输出序列中的距离 [2, 19]。然而，除少数情况外 [27]，此类注意力机制都是与循环网络结合使用的。

> In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output. The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs.

在本工作中，我们提出 **Transformer**：一种摒弃循环、转而完全依赖注意力机制来刻画输入与输出之间全局依赖关系的模型架构。Transformer 允许显著更高程度的并行化，并且只需在 8 块 P100 GPU 上训练 12 小时，就能在翻译质量上达到新的最先进水平。

---

## 2 背景 / Background

> The goal of reducing sequential computation also forms the foundation of the Extended Neural GPU [16], ByteNet [18] and ConvS2S [9], all of which use convolutional neural networks as basic building block, computing hidden representations in parallel for all input and output positions. In these models, the number of operations required to relate signals from two arbitrary input or output positions grows in the distance between positions, linearly for ConvS2S and logarithmically for ByteNet. This makes it more difficult to learn dependencies between distant positions [12]. In the Transformer this is reduced to a constant number of operations, albeit at the cost of reduced effective resolution due to averaging attention-weighted positions, an effect we counteract with Multi-Head Attention as described in section 3.2.

减少顺序计算这一目标，同样是扩展神经 GPU（Extended Neural GPU）[16]、ByteNet [18] 和 ConvS2S [9] 的基础，它们都以卷积神经网络作为基本构建模块，为所有输入和输出位置并行计算隐表示。在这些模型中，关联任意两个输入或输出位置信号所需的操作数随位置间距离增长：ConvS2S 为线性增长，ByteNet 为对数增长。这使得学习相距较远位置之间的依赖关系更加困难 [12]。在 Transformer 中，这一操作数被降至常数级，代价是由于对注意力加权位置取平均而导致有效分辨率降低；我们通过 3.2 节所述的多头注意力来抵消这一影响。

> Self-attention, sometimes called intra-attention is an attention mechanism relating different positions of a single sequence in order to compute a representation of the sequence. Self-attention has been used successfully in a variety of tasks including reading comprehension, abstractive summarization, textual entailment and learning task-independent sentence representations [4, 27, 28, 22].

自注意力（有时称为内部注意力，intra-attention）是一种将单一序列中不同位置相互关联、以计算该序列表示的注意力机制。自注意力已在多种任务中被成功使用，包括阅读理解、生成式摘要、文本蕴含以及学习与任务无关的句子表示 [4, 27, 28, 22]。

> End-to-end memory networks are based on a recurrent attention mechanism instead of sequence-aligned recurrence and have been shown to perform well on simple-language question answering and language modeling tasks [34].

端到端记忆网络基于循环注意力机制而非序列对齐的循环结构，已被证明在简单语言问答和语言建模任务上表现良好 [34]。

> To the best of our knowledge, however, the Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequence-aligned RNNs or convolution. In the following sections, we will describe the Transformer, motivate self-attention and discuss its advantages over models such as [17, 18] and [9].

然而，据我们所知，Transformer 是第一个完全依赖自注意力来计算其输入与输出表示、而不使用序列对齐 RNN 或卷积的转导模型。在接下来的各节中，我们将描述 Transformer，阐述采用自注意力的动机，并讨论它相对于 [17, 18] 和 [9] 等模型的优势。

---

## 3 模型架构 / Model Architecture

> Most competitive neural sequence transduction models have an encoder-decoder structure [5, 2, 35]. Here, the encoder maps an input sequence of symbol representations (x_1, ..., x_n) to a sequence of continuous representations z = (z_1, ..., z_n). Given z, the decoder then generates an output sequence (y_1, ..., y_m) of symbols one element at a time. At each step the model is auto-regressive [10], consuming the previously generated symbols as additional input when generating the next.

大多数有竞争力的神经序列转导模型都具有编码器-解码器结构 [5, 2, 35]。在这里，编码器将输入的符号表示序列 (x_1, ..., x_n) 映射为连续表示序列 z = (z_1, ..., z_n)。给定 z 后，解码器逐个元素地生成符号输出序列 (y_1, ..., y_m)。每一步中模型都是自回归的 [10]，即在生成下一个符号时，把先前生成的符号作为额外输入加以利用。

> Figure 1: The Transformer - model architecture.

**图 1：Transformer —— 模型架构。**

![图 1 / Figure 1：Transformer 模型架构](/assets/attention/fig1_transformer_architecture.png)

> The Transformer follows this overall architecture using stacked self-attention and point-wise, fully connected layers for both the encoder and decoder, shown in the left and right halves of Figure 1, respectively.

Transformer 对编码器和解码器都采用堆叠的自注意力层与逐位置全连接层来贯彻这一整体架构，二者分别如图 1 的左半部分和右半部分所示。

### 3.1 编码器与解码器堆栈 / Encoder and Decoder Stacks

> **Encoder:** The encoder is composed of a stack of N = 6 identical layers. Each layer has two sub-layers. The first is a multi-head self-attention mechanism, and the second is a simple, position-wise fully connected feed-forward network. We employ a residual connection [11] around each of the two sub-layers, followed by layer normalization [1]. That is, the output of each sub-layer is LayerNorm(x + Sublayer(x)), where Sublayer(x) is the function implemented by the sub-layer itself. To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension d_model = 512.

**编码器：** 编码器由 N = 6 个相同层堆叠而成。每一层包含两个子层。第一个是多头自注意力机制，第二个是简单的、逐位置的全连接前馈网络。我们在两个子层中的每一个周围都使用一个残差连接 [11]，随后进行层归一化 [1]。也就是说，每个子层的输出为 LayerNorm(x + Sublayer(x))，其中 Sublayer(x) 是该子层自身所实现的函数。为便于这些残差连接，模型中的所有子层以及嵌入层都产生维度为 d_model = 512 的输出。

> **Decoder:** The decoder is also composed of a stack of N = 6 identical layers. In addition to the two sub-layers in each encoder layer, the decoder inserts a third sub-layer, which performs multi-head attention over the output of the encoder stack. Similar to the encoder, we employ residual connections around each of the sub-layers, followed by layer normalization. We also modify the self-attention sub-layer in the decoder stack to prevent positions from attending to subsequent positions. This masking, combined with fact that the output embeddings are offset by one position, ensures that the predictions for position i can depend only on the known outputs at positions less than i.

**解码器：** 解码器同样由 N = 6 个相同层堆叠而成。除了每个编码器层中的两个子层之外，解码器还插入了第三个子层，它对编码器堆栈的输出执行多头注意力。与编码器类似，我们在每个子层周围使用残差连接，随后进行层归一化。我们还修改了解码器堆栈中的自注意力子层，以防止某些位置关注其后的位置。这种掩蔽，再加上输出嵌入被偏移一个位置这一事实，确保了位置 i 的预测只能依赖于小于 i 的位置上已知的输出。

### 3.2 注意力 / Attention

> An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors. The output is computed as a weighted sum of the values, where the weight assigned to each value is computed by a compatibility function of the query with the corresponding key.

注意力函数可以描述为：将一个查询（query）和一组键-值（key-value）对映射为一个输出，其中查询、键、值和输出均为向量。输出按值的加权和计算，而赋予每个值的权重，由查询与相应键之间的兼容性函数计算得到。

> Figure 2: (left) Scaled Dot-Product Attention. (right) Multi-Head Attention consists of several attention layers running in parallel.

**图 2：（左）缩放点积注意力。（右）多头注意力由若干并行运行的注意力层组成。**

![图 2a / Figure 2 left：缩放点积注意力](/assets/attention/fig2a_scaled_dot_product_attention.png)

![图 2b / Figure 2 right：多头注意力](/assets/attention/fig2b_multi_head_attention.png)

#### 3.2.1 缩放点积注意力 / Scaled Dot-Product Attention

> We call our particular attention "Scaled Dot-Product Attention" (Figure 2). The input consists of queries and keys of dimension d_k, and values of dimension d_v. We compute the dot products of the query with all keys, divide each by √d_k, and apply a softmax function to obtain the weights on the values.

我们称本文所采用的这种特定注意力为"缩放点积注意力"（Scaled Dot-Product Attention，图 2）。其输入由维度为 d_k 的查询和键，以及维度为 d_v 的值组成。我们计算查询与所有键的点积，将每一个除以 √d_k，再应用 softmax 函数，从而得到各值上的权重。

> In practice, we compute the attention function on a set of queries simultaneously, packed together into a matrix Q. The keys and values are also packed together into matrices K and V. We compute the matrix of outputs as:

在实践中，我们同时对一组查询计算注意力函数，将它们打包进矩阵 Q。键和值也同样被打包为矩阵 K 和 V。我们按下式计算输出矩阵：

> **Attention(Q, K, V) = softmax(QK^T / √d_k) V**　　(1)

**Attention(Q, K, V) = softmax(QK^T / √d_k) V**　　(1)

> The two most commonly used attention functions are additive attention [2], and dot-product (multiplicative) attention. Dot-product attention is identical to our algorithm, except for the scaling factor of 1/√d_k. Additive attention computes the compatibility function using a feed-forward network with a single hidden layer. While the two are similar in theoretical complexity, dot-product attention is much faster and more space-efficient in practice, since it can be implemented using highly optimized matrix multiplication code.

最常用的两种注意力函数是加性注意力 [2] 与点积（乘性）注意力。除缩放因子 1/√d_k 之外，点积注意力与我们的算法完全相同。加性注意力使用带单个隐藏层的前馈网络来计算兼容性函数。两者在理论复杂度上相近，但在实践中点积注意力要快得多、也更节省空间，因为它可以用高度优化的矩阵乘法代码来实现。

> While for small values of d_k the two mechanisms perform similarly, additive attention outperforms dot product attention without scaling for larger values of d_k [3]. We suspect that for large values of d_k, the dot products grow large in magnitude, pushing the softmax function into regions where it has extremely small gradients⁴. To counteract this effect, we scale the dot products by 1/√d_k.

当 d_k 取值较小时，两种机制表现相近；但对于较大的 d_k，若不加缩放，加性注意力的表现会优于点积注意力 [3]。我们推测，当 d_k 较大时，点积的幅值会变得很大，从而把 softmax 函数推入梯度极小的区域⁴。为抵消这一影响，我们以 1/√d_k 对点积进行缩放。

> ⁴To illustrate why the dot products get large, assume that the components of q and k are independent random variables with mean 0 and variance 1. Then their dot product, q · k = Σ(d_k, i=1) q_i k_i, has mean 0 and variance d_k.

⁴ 为说明点积为何会变大，假设 q 与 k 的各分量是均值为 0、方差为 1 的独立随机变量。那么它们的点积 q · k = Σ_{i=1}^{d_k} q_i k_i 的均值为 0，方差为 d_k。

#### 3.2.2 多头注意力 / Multi-Head Attention

> Instead of performing a single attention function with d_model-dimensional keys, values and queries, we found it beneficial to linearly project the queries, keys and values h times with different, learned linear projections to d_k, d_k and d_v dimensions, respectively. On each of these projected versions of queries, keys and values we then perform the attention function in parallel, yielding d_v-dimensional output values. These are concatenated and once again projected, resulting in the final values, as depicted in Figure 2.

与使用 d_model 维的键、值和查询执行单一的注意力函数不同，我们发现：用不同的、可学习的线性投影把查询、键和值分别线性投影 h 次、映射到 d_k、d_k 和 d_v 维，是有益的。随后，我们对这些投影后的查询、键和值并行地执行注意力函数，得到 d_v 维的输出值。这些输出值被拼接起来并再次投影，得到最终的值，如图 2 所示。

> Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions. With a single attention head, averaging inhibits this.

多头注意力使模型能够联合关注来自不同表示子空间、不同位置的信息。若只有一个注意力头，取平均会抑制这种能力。

> **MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O**
> **where head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V)**

**MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O**
**其中 head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V)**

> Where the projections are parameter matrices W_i^Q ∈ R^(d_model×d_k), W_i^K ∈ R^(d_model×d_k), W_i^V ∈ R^(d_model×d_v) and W^O ∈ R^(h d_v×d_model).

其中各投影为参数矩阵：W_i^Q ∈ R^(d_model×d_k)，W_i^K ∈ R^(d_model×d_k)，W_i^V ∈ R^(d_model×d_v)，以及 W^O ∈ R^(h d_v×d_model)。

> In this work we employ h = 8 parallel attention layers, or heads. For each of these we use d_k = d_v = d_model/h = 64. Due to the reduced dimension of each head, the total computational cost is similar to that of single-head attention with full dimensionality.

在本工作中，我们采用 h = 8 个并行的注意力层，即 8 个注意力头。对于每一个头，我们取 d_k = d_v = d_model/h = 64。由于每个头的维度降低，总计算成本与全维度的单头注意力相近。

#### 3.2.3 注意力在本模型中的应用 / Applications of Attention in our Model

> The Transformer uses multi-head attention in three different ways:

Transformer 以三种不同的方式使用多头注意力：

> • In "encoder-decoder attention" layers, the queries come from the previous decoder layer, and the memory keys and values come from the output of the encoder. This allows every position in the decoder to attend over all positions in the input sequence. This mimics the typical encoder-decoder attention mechanisms in sequence-to-sequence models such as [38, 2, 9].

- 在"编码器-解码器注意力"层中，查询来自前一个解码器层，而记忆（memory）的键和值来自编码器的输出。这使解码器中的每个位置都能关注输入序列中的所有位置。这模仿了 [38, 2, 9] 等序列到序列模型中典型的编码器-解码器注意力机制。

> • The encoder contains self-attention layers. In a self-attention layer all of the keys, values and queries come from the same place, in this case, the output of the previous layer in the encoder. Each position in the encoder can attend to all positions in the previous layer of the encoder.

- 编码器中包含自注意力层。在自注意力层里，所有的键、值和查询都来自同一处，在此即编码器中前一层的输出。编码器中的每个位置都可以关注编码器前一层的所有位置。

> • Similarly, self-attention layers in the decoder allow each position in the decoder to attend to all positions in the decoder up to and including that position. We need to prevent leftward information flow in the decoder to preserve the auto-regressive property. We implement this inside of scaled dot-product attention by masking out (setting to −∞) all values in the input of the softmax which correspond to illegal connections. See Figure 2.

- 类似地，解码器中的自注意力层允许解码器中的每个位置关注解码器中直到并包括该位置在内的所有位置。我们需要阻止解码器中的信息向左流动，以保持自回归特性。我们在缩放点积注意力内部实现这一点：把 softmax 输入中所有对应非法连接的值掩蔽掉（设为 −∞）。参见图 2。

### 3.3 逐位置前馈网络 / Position-wise Feed-Forward Networks

> In addition to attention sub-layers, each of the layers in our encoder and decoder contains a fully connected feed-forward network, which is applied to each position separately and identically. This consists of two linear transformations with a ReLU activation in between.

除注意力子层之外，我们的编码器和解码器中的每一层还包含一个全连接前馈网络，它对每个位置分别地、以相同方式施加。该网络由两次线性变换构成，中间夹有一个 ReLU 激活。

> **FFN(x) = max(0, xW_1 + b_1) W_2 + b_2**　　(2)

**FFN(x) = max(0, xW_1 + b_1) W_2 + b_2**　　(2)

> While the linear transformations are the same across different positions, they use different parameters from layer to layer. Another way of describing this is as two convolutions with kernel size 1. The dimensionality of input and output is d_model = 512, and the inner-layer has dimensionality d_ff = 2048.

虽然线性变换在不同位置之间是相同的，但它们在层与层之间使用不同的参数。另一种描述方式是：把它看作两个卷积核大小为 1 的卷积。输入和输出的维度为 d_model = 512，内层的维度为 d_ff = 2048。

### 3.4 嵌入与 Softmax / Embeddings and Softmax

> Similarly to other sequence transduction models, we use learned embeddings to convert the input tokens and output tokens to vectors of dimension d_model. We also use the usual learned linear transformation and softmax function to convert the decoder output to predicted next-token probabilities. In our model, we share the same weight matrix between the two embedding layers and the pre-softmax linear transformation, similar to [30]. In the embedding layers, we multiply those weights by √d_model.

与其他序列转导模型类似，我们使用可学习的嵌入把输入词元和输出词元转换为维度为 d_model 的向量。我们还使用通常的可学习线性变换和 softmax 函数，把解码器输出转换为下一个词元的预测概率。在我们的模型中，两个嵌入层与 softmax 之前的线性变换共享同一个权重矩阵，这与 [30] 类似。在嵌入层中，我们将这些权重乘以 √d_model。

> Table 1: Maximum path lengths, per-layer complexity and minimum number of sequential operations for different layer types. n is the sequence length, d is the representation dimension, k is the kernel size of convolutions and r is the size of the neighborhood in restricted self-attention.

**表 1：不同层类型的最大路径长度、每层复杂度与最少顺序操作数。** 其中 n 是序列长度，d 是表示维度，k 是卷积核大小，r 是受限自注意力中邻域的大小。

| 层类型<br>Layer Type | 每层复杂度<br>Complexity per Layer | 顺序操作数<br>Sequential Operations | 最大路径长度<br>Maximum Path Length |
| --- | --- | --- | --- |
| 自注意力<br>Self-Attention | O(n² · d) | O(1) | O(1) |
| 循环<br>Recurrent | O(n · d²) | O(n) | O(n) |
| 卷积<br>Convolutional | O(k · n · d²) | O(1) | O(log_k(n)) |
| 自注意力（受限）<br>Self-Attention (restricted) | O(r · n · d) | O(1) | O(n/r) |

### 3.5 位置编码 / Positional Encoding

> Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence. To this end, we add "positional encodings" to the input embeddings at the bottoms of the encoder and decoder stacks. The positional encodings have the same dimension d_model as the embeddings, so that the two can be summed. There are many choices of positional encodings, learned and fixed [9].

由于我们的模型既不包含循环也不包含卷积，为了让模型能够利用序列的顺序，我们必须注入关于序列中词元相对或绝对位置的信息。为此，我们在编码器和解码器堆栈底部，把"位置编码"加到输入嵌入上。位置编码与嵌入具有相同的维度 d_model，因此二者可以直接相加。位置编码有多种选择，既可以是可学习的，也可以是固定的 [9]。

> In this work, we use sine and cosine functions of different frequencies:

在本工作中，我们使用不同频率的正弦和余弦函数：

> **PE(pos, 2i) = sin(pos / 10000^(2i/d_model))**
> **PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))**

**PE(pos, 2i) = sin(pos / 10000^(2i/d_model))**
**PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))**

> where pos is the position and i is the dimension. That is, each dimension of the positional encoding corresponds to a sinusoid. The wavelengths form a geometric progression from 2π to 10000 · 2π. We chose this function because we hypothesized it would allow the model to easily learn to attend by relative positions, since for any fixed offset k, PE_(pos+k) can be represented as a linear function of PE_pos.

其中 pos 是位置，i 是维度。也就是说，位置编码的每个维度都对应一条正弦曲线。其波长构成一个从 2π 到 10000 · 2π 的等比数列。我们选择这一函数，是因为我们假设它能让模型容易地学会按相对位置进行关注：对于任意固定的偏移量 k，PE_(pos+k) 都可以表示为 PE_pos 的线性函数。

> We also experimented with using learned positional embeddings [9] instead, and found that the two versions produced nearly identical results (see Table 3 row (E)). We chose the sinusoidal version because it may allow the model to extrapolate to sequence lengths longer than the ones encountered during training.

我们也试验了改用可学习的位置嵌入 [9]，发现两种版本产生的结果几乎完全一致（见表 3 第 (E) 行）。我们选择正弦版本，是因为它可能使模型能够外推到比训练时遇到的更长的序列长度。

---

## 4 为什么使用自注意力 / Why Self-Attention

> In this section we compare various aspects of self-attention layers to the recurrent and convolutional layers commonly used for mapping one variable-length sequence of symbol representations (x_1, ..., x_n) to another sequence of equal length (z_1, ..., z_n), with x_i, z_i ∈ R^d, such as a hidden layer in a typical sequence transduction encoder or decoder. Motivating our use of self-attention we consider three desiderata.

在本节中，我们将自注意力层的各个方面，与常用于把一个变长符号表示序列 (x_1, ..., x_n) 映射为另一个等长序列 (z_1, ..., z_n)（其中 x_i, z_i ∈ R^d）的循环层和卷积层进行比较；这里的序列可以理解为典型序列转导编码器或解码器中的某个隐藏层。为说明我们采用自注意力的动机，我们考虑三项期望指标。

> One is the total computational complexity per layer. Another is the amount of computation that can be parallelized, as measured by the minimum number of sequential operations required.

其一是每层的总计算复杂度。其二是可并行化的计算量，用所需的最少顺序操作数来衡量。

> The third is the path length between long-range dependencies in the network. Learning long-range dependencies is a key challenge in many sequence transduction tasks. One key factor affecting the ability to learn such dependencies is the length of the paths forward and backward signals have to traverse in the network. The shorter these paths between any combination of positions in the input and output sequences, the easier it is to learn long-range dependencies [12]. Hence we also compare the maximum path length between any two input and output positions in networks composed of the different layer types.

其三，是网络中长程依赖之间的路径长度。学习长程依赖是许多序列转导任务中的关键挑战。影响学习此类依赖能力的一个关键因素，是前向与后向信号在网络中必须经过的路径长度。输入和输出序列中任意位置组合之间的这些路径越短，学习长程依赖就越容易 [12]。因此，我们还比较了由不同层类型构成的网络中，任意两个输入与输出位置之间的最大路径长度。

> As noted in Table 1, a self-attention layer connects all positions with a constant number of sequentially executed operations, whereas a recurrent layer requires O(n) sequential operations. In terms of computational complexity, self-attention layers are faster than recurrent layers when the sequence length n is smaller than the representation dimensionality d, which is most often the case with sentence representations used by state-of-the-art models in machine translations, such as word-piece [38] and byte-pair [31] representations. To improve computational performance for tasks involving very long sequences, self-attention could be restricted to considering only a neighborhood of size r in the input sequence centered around the respective output position. This would increase the maximum path length to O(n/r). We plan to investigate this approach further in future work.

如表 1 所示，自注意力层用常数个顺序执行的操作连接所有位置，而循环层需要 O(n) 个顺序操作。就计算复杂度而言，当序列长度 n 小于表示维度 d 时，自注意力层比循环层更快；而在机器翻译中最先进模型所使用的句子表示（如 word-piece [38] 和 byte-pair [31] 表示）中，这通常正是实际情况。为提升涉及极长序列任务的计算性能，可以把自注意力限制为只考虑输入序列中以相应输出位置为中心、大小为 r 的邻域。这会把最大路径长度增加到 O(n/r)。我们计划在未来工作中进一步研究这一思路。

> A single convolutional layer with kernel width k < n does not connect all pairs of input and output positions. Doing so requires a stack of O(n/k) convolutional layers in the case of contiguous kernels, or O(log_k(n)) in the case of dilated convolutions [18], increasing the length of the longest paths between any two positions in the network. Convolutional layers are generally more expensive than recurrent layers, by a factor of k. Separable convolutions [6], however, decrease the complexity considerably, to O(k · n · d + n · d²). Even with k = n, however, the complexity of a separable convolution is equal to the combination of a self-attention layer and a point-wise feed-forward layer, the approach we take in our model.

当卷积核宽度 k < n 时，单个卷积层无法连接所有输入与输出位置对。要做到这一点，在连续卷积核的情况下需要 O(n/k) 个卷积层堆叠，在空洞卷积 [18] 的情况下需要 O(log_k(n)) 个，这都会增加网络中任意两个位置之间最长路径的长度。卷积层通常比循环层昂贵，代价高出 k 倍。不过，可分离卷积 [6] 把复杂度显著降低到 O(k · n · d + n · d²)。然而，即使 k = n，可分离卷积的复杂度也等同于自注意力层与逐位置前馈层的组合，而这正是我们模型所采用的做法。

> As side benefit, self-attention could yield more interpretable models. We inspect attention distributions from our models and present and discuss examples in the appendix. Not only do individual attention heads clearly learn to perform different tasks, many appear to exhibit behavior related to the syntactic and semantic structure of the sentences.

作为一个附带的好处，自注意力还可能带来更具可解释性的模型。我们检查了模型的注意力分布，并在附录中给出并讨论了若干示例。各个注意力头不仅清晰地学会了执行不同的任务，其中许多还表现出与句子的句法和语义结构相关的行为。

---

## 5 训练 / Training

> This section describes the training regime for our models.

本节描述我们模型的训练方案。

### 5.1 训练数据与批处理 / Training Data and Batching

> We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million sentence pairs. Sentences were encoded using byte-pair encoding [3], which has a shared source-target vocabulary of about 37000 tokens. For English-French, we used the significantly larger WMT 2014 English-French dataset consisting of 36M sentences and split tokens into a 32000 word-piece vocabulary [38]. Sentence pairs were batched together by approximate sequence length. Each training batch contained a set of sentence pairs containing approximately 25000 source tokens and 25000 target tokens.

我们在标准的 WMT 2014 英德数据集上进行训练，该数据集包含约 450 万个句子对。句子使用字节对编码（byte-pair encoding）[3] 进行编码，其源语言-目标语言共享词表约含 37000 个词元。对于英法翻译，我们使用了规模显著更大的 WMT 2014 英法数据集，包含 3600 万个句子，并将词元切分为 32000 个 word-piece 的词表 [38]。句子对按近似序列长度打包成批。每个训练批次包含一组句子对，其中约含 25000 个源语言词元和 25000 个目标语言词元。

### 5.2 硬件与训练计划 / Hardware and Schedule

> We trained our models on one machine with 8 NVIDIA P100 GPUs. For our base models using the hyperparameters described throughout the paper, each training step took about 0.4 seconds. We trained the base models for a total of 100,000 steps or 12 hours. For our big models,(described on the bottom line of table 3), step time was 1.0 seconds. The big models were trained for 300,000 steps (3.5 days).

我们在一台配备 8 块 NVIDIA P100 GPU 的机器上训练模型。对于使用本文所述超参数的 base 模型，每个训练步约耗时 0.4 秒。base 模型共训练 100,000 步，即 12 小时。对于 big 模型（见表 3 最下面一行），每步耗时为 1.0 秒。big 模型训练了 300,000 步（3.5 天）。

### 5.3 优化器 / Optimizer

> We used the Adam optimizer [20] with β_1 = 0.9, β_2 = 0.98 and ϵ = 10^−9. We varied the learning rate over the course of training, according to the formula:

我们使用 Adam 优化器 [20]，取 β_1 = 0.9、β_2 = 0.98、ϵ = 10^−9。我们在训练过程中按下式改变学习率：

> **lrate = d_model^(−0.5) · min(step_num^(−0.5), step_num · warmup_steps^(−1.5))**　　(3)

**lrate = d_model^(−0.5) · min(step_num^(−0.5), step_num · warmup_steps^(−1.5))**　　(3)

> This corresponds to increasing the learning rate linearly for the first warmup_steps training steps, and decreasing it thereafter proportionally to the inverse square root of the step number. We used warmup_steps = 4000.

这相当于：在前 warmup_steps 个训练步中线性地提高学习率，此后按步数的平方根倒数成比例地降低学习率。我们取 warmup_steps = 4000。

### 5.4 正则化 / Regularization

> We employ three types of regularization during training:

我们在训练期间采用三种正则化手段：

> **Residual Dropout** We apply dropout [33] to the output of each sub-layer, before it is added to the sub-layer input and normalized. In addition, we apply dropout to the sums of the embeddings and the positional encodings in both the encoder and decoder stacks. For the base model, we use a rate of P_drop = 0.1.

**残差 Dropout** 我们对每个子层的输出施加 dropout [33]，施加位置在该输出被加到子层输入并进行归一化之前。此外，我们还对编码器和解码器堆栈中嵌入与位置编码之和施加 dropout。对于 base 模型，我们使用比率 P_drop = 0.1。

> **Label Smoothing** During training, we employed label smoothing of value ϵ_ls = 0.1 [36]. This hurts perplexity, as the model learns to be more unsure, but improves accuracy and BLEU score.

**标签平滑（Label Smoothing）** 训练期间我们采用取值 ϵ_ls = 0.1 的标签平滑 [36]。这会损害困惑度（因为模型学会了更加"不确定"），但能提升准确率和 BLEU 分数。

> Table 2: The Transformer achieves better BLEU scores than previous state-of-the-art models on the English-to-German and English-to-French newstest2014 tests at a fraction of the training cost.

**表 2：在英德与英法 newstest2014 测试集上，Transformer 以仅为先前模型一小部分的训练成本，取得了比此前最先进模型更好的 BLEU 分数。**

| 模型<br>Model | BLEU<br>EN-DE | BLEU<br>EN-FR | 训练成本 Training Cost (FLOPs)<br>EN-DE | 训练成本 Training Cost (FLOPs)<br>EN-FR |
| --- | --- | --- | --- | --- |
| ByteNet [18] | 23.75 | | | |
| Deep-Att + PosUnk [39] | | 39.2 | | 1.0 · 10²⁰ |
| GNMT + RL [38] | 24.6 | 39.92 | 2.3 · 10¹⁹ | 1.4 · 10²⁰ |
| ConvS2S [9] | 25.16 | 40.46 | 9.6 · 10¹⁸ | 1.5 · 10²⁰ |
| MoE [32] | 26.03 | 40.56 | 2.0 · 10¹⁹ | 1.2 · 10²⁰ |
| Deep-Att + PosUnk Ensemble [39] | | 40.4 | | 8.0 · 10²⁰ |
| GNMT + RL Ensemble [38] | 26.30 | 41.16 | 1.8 · 10²⁰ | 1.1 · 10²¹ |
| ConvS2S Ensemble [9] | 26.36 | 41.29 | 7.7 · 10¹⁹ | 1.2 · 10²¹ |
| **Transformer (base model)** | **27.3** | **38.1** | **3.3 · 10¹⁸** | |
| **Transformer (big)** | **28.4** | **41.8** | **2.3 · 10¹⁹** | |

---

## 6 结果 / Results

### 6.1 机器翻译 / Machine Translation

> On the WMT 2014 English-to-German translation task, the big transformer model (Transformer (big) in Table 2) outperforms the best previously reported models (including ensembles) by more than 2.0 BLEU, establishing a new state-of-the-art BLEU score of 28.4. The configuration of this model is listed in the bottom line of Table 3. Training took 3.5 days on 8 P100 GPUs. Even our base model surpasses all previously published models and ensembles, at a fraction of the training cost of any of the competitive models.

在 WMT 2014 英德翻译任务上，big transformer 模型（表 2 中的 Transformer (big)）比此前报告的最佳模型（包括集成模型）高出 2.0 BLEU 以上，创下 28.4 的新的最先进 BLEU 分数。该模型的配置列于表 3 最下面一行。训练在 8 块 P100 GPU 上耗时 3.5 天。即便是我们的 base 模型，也以远低于任何竞争模型训练成本的一小部分，超越了此前发表的所有模型与集成模型。

> On the WMT 2014 English-to-French translation task, our big model achieves a BLEU score of 41.0, outperforming all of the previously published single models, at less than 1/4 the training cost of the previous state-of-the-art model. The Transformer (big) model trained for English-to-French used dropout rate P_drop = 0.1, instead of 0.3.

在 WMT 2014 英法翻译任务上，我们的 big 模型取得 41.0 的 BLEU 分数，超越了此前发表的所有单模型，而其训练成本不到此前最先进模型的 1/4。用于英法翻译训练的 Transformer (big) 模型使用了 dropout 比率 P_drop = 0.1，而非 0.3。

> For the base models, we used a single model obtained by averaging the last 5 checkpoints, which were written at 10-minute intervals. For the big models, we averaged the last 20 checkpoints. We used beam search with a beam size of 4 and length penalty α = 0.6 [38]. These hyperparameters were chosen after experimentation on the development set. We set the maximum output length during inference to input length + 50, but terminate early when possible [38].

对于 base 模型，我们使用对最后 5 个检查点取平均所得到的单一模型，这些检查点每 10 分钟保存一次。对于 big 模型，我们对最后 20 个检查点取平均。我们使用束搜索（beam search），束宽为 4，长度惩罚 α = 0.6 [38]。这些超参数是在开发集上经过实验后选定的。我们把推理时的最大输出长度设为输入长度 + 50，但在可能时提前终止 [38]。

> Table 2 summarizes our results and compares our translation quality and training costs to other model architectures from the literature. We estimate the number of floating point operations used to train a model by multiplying the training time, the number of GPUs used, and an estimate of the sustained single-precision floating-point capacity of each GPU⁵.

表 2 总结了我们的结果，并将我们的翻译质量与训练成本同文献中的其他模型架构进行了比较。我们估计训练一个模型所用的浮点运算次数的方法是：把训练时间、所用 GPU 数量，以及每块 GPU 持续单精度浮点运算能力的估计值三者相乘⁵。

> ⁵We used values of 2.8, 3.7, 6.0 and 9.5 TFLOPS for K80, K40, M40 and P100, respectively.

⁵ 对于 K80、K40、M40 和 P100，我们分别采用了 2.8、3.7、6.0 和 9.5 TFLOPS 的数值。

### 6.2 模型变体 / Model Variations

> To evaluate the importance of different components of the Transformer, we varied our base model in different ways, measuring the change in performance on English-to-German translation on the development set, newstest2013. We used beam search as described in the previous section, but no checkpoint averaging. We present these results in Table 3.

为评估 Transformer 各个组成部分的重要性，我们以不同方式对 base 模型加以变动，并测量其在开发集 newstest2013 上英德翻译性能的变化。我们使用上一节所述的束搜索，但不做检查点平均。这些结果列于表 3。

> Table 3: Variations on the Transformer architecture. Unlisted values are identical to those of the base model. All metrics are on the English-to-German translation development set, newstest2013. Listed perplexities are per-wordpiece, according to our byte-pair encoding, and should not be compared to per-word perplexities.

**表 3：Transformer 架构的各种变体。** 未列出的取值与 base 模型相同。所有指标均在英德翻译开发集 newstest2013 上测得。所列困惑度为按我们的字节对编码计算的逐 word-piece 困惑度，不应与逐词困惑度相比较。

| 变体<br>Variant | N | d_model | d_ff | h | d_k | d_v | P_drop | ϵ_ls | 训练步数<br>train steps | PPL<br>(dev) | BLEU<br>(dev) | 参数量<br>params ×10⁶ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | 6 | 512 | 2048 | 8 | 64 | 64 | 0.1 | 0.1 | 100K | 4.92 | 25.8 | 65 |
| (A) | | | | 1 | 512 | 512 | | | | 5.29 | 24.9 | |
| | | | | 4 | 128 | 128 | | | | 5.00 | 25.5 | |
| | | | | 16 | 32 | 32 | | | | 4.91 | 25.8 | |
| | | | | 32 | 16 | 16 | | | | 5.01 | 25.4 | |
| (B) | | | | 16 | | | | | | 5.16 | 25.1 | 58 |
| | | | | 32 | | | | | | 5.01 | 25.4 | 60 |
| (C) | 2 | | | | | | | | | 6.11 | 23.7 | 36 |
| | 4 | | | | | | | | | 5.19 | 25.3 | 50 |
| | 8 | | | | | | | | | 4.88 | 25.5 | 80 |
| | | 256 | | | 32 | 32 | | | | 5.75 | 24.5 | 28 |
| | | 1024 | | | 128 | 128 | | | | 4.66 | 26.0 | 168 |
| | | | 1024 | | | | | | | 5.12 | 25.4 | 53 |
| | | | 4096 | | | | | | | 4.75 | 26.2 | 90 |
| (D) | | | | | | | 0.0 | | | 5.77 | 24.6 | |
| | | | | | | | 0.2 | | | 4.95 | 25.5 | |
| | | | | | | | | 0.0 | | 4.67 | 25.3 | |
| | | | | | | | | 0.2 | | 5.47 | 25.7 | |
| (E) | 用可学习的位置嵌入替代正弦编码<br>positional embedding instead of sinusoids ※ | | | | | | | | | 4.92 | 25.7 | |
| big | 6 | 1024 | 4096 | 16 | | | 0.3 | | 300K | 4.33 | 26.4 | 213 |

※ 原表中该说明横向跨越 N 至 train steps 各列。

> In Table 3 rows (A), we vary the number of attention heads and the attention key and value dimensions, keeping the amount of computation constant, as described in Section 3.2.2. While single-head attention is 0.9 BLEU worse than the best setting, quality also drops off with too many heads.

在表 3 的 (A) 组各行中，我们按 3.2.2 节所述，在保持计算量不变的前提下变动注意力头数以及注意力的键、值维度。单头注意力比最佳设置差 0.9 BLEU，而注意力头过多时质量同样会下降。

> In Table 3 rows (B), we observe that reducing the attention key size d_k hurts model quality. This suggests that determining compatibility is not easy and that a more sophisticated compatibility function than dot product may be beneficial. We further observe in rows (C) and (D) that, as expected, bigger models are better, and dropout is very helpful in avoiding over-fitting. In row (E) we replace our sinusoidal positional encoding with learned positional embeddings [9], and observe nearly identical results to the base model.

在表 3 的 (B) 组各行中，我们观察到减小注意力键的维度 d_k 会损害模型质量。这表明确定兼容性并非易事，采用比点积更精细的兼容性函数可能是有益的。我们进一步在 (C) 和 (D) 组中观察到：如预期的那样，更大的模型更好，而 dropout 对避免过拟合非常有帮助。在 (E) 行中，我们用可学习的位置嵌入 [9] 替换正弦位置编码，观察到结果与 base 模型几乎完全相同。

### 6.3 英语成分句法分析 / English Constituency Parsing

> To evaluate if the Transformer can generalize to other tasks we performed experiments on English constituency parsing. This task presents specific challenges: the output is subject to strong structural constraints and is significantly longer than the input. Furthermore, RNN sequence-to-sequence models have not been able to attain state-of-the-art results in small-data regimes [37].

为评估 Transformer 能否泛化到其他任务，我们在英语成分句法分析上进行了实验。该任务有其特定的挑战：输出受到很强的结构约束，而且显著长于输入。此外，RNN 序列到序列模型在数据量较少的情形下一直未能达到最先进的结果 [37]。

> We trained a 4-layer transformer with d_model = 1024 on the Wall Street Journal (WSJ) portion of the Penn Treebank [25], about 40K training sentences. We also trained it in a semi-supervised setting, using the larger high-confidence and BerkleyParser corpora from with approximately 17M sentences [37]. We used a vocabulary of 16K tokens for the WSJ only setting and a vocabulary of 32K tokens for the semi-supervised setting.

我们在宾州树库（Penn Treebank）[25] 的《华尔街日报》（WSJ）部分上训练了一个 4 层、d_model = 1024 的 Transformer，约含 4 万条训练句子。我们还在半监督设置下训练它，使用规模更大的 high-confidence 与 BerkleyParser 语料，约含 1700 万条句子 [37]。在仅用 WSJ 的设置下，我们使用 16K 词元的词表；在半监督设置下使用 32K 词元的词表。

> We performed only a small number of experiments to select the dropout, both attention and residual (section 5.4), learning rates and beam size on the Section 22 development set, all other parameters remained unchanged from the English-to-German base translation model. During inference, we increased the maximum output length to input length + 300. We used a beam size of 21 and α = 0.3 for both WSJ only and the semi-supervised setting.

我们只在第 22 节开发集上做了少量实验，以选择 dropout（包括注意力和残差 dropout，见 5.4 节）、学习率和束宽；其余所有参数都保持与英德 base 翻译模型相同。在推理时，我们把最大输出长度增加到输入长度 + 300。无论仅用 WSJ 还是半监督设置，我们都使用束宽 21 和 α = 0.3。

> Table 4: The Transformer generalizes well to English constituency parsing (Results are on Section 23 of WSJ)

**表 4：Transformer 能很好地泛化到英语成分句法分析（结果基于 WSJ 第 23 节）。**

| 句法分析器<br>Parser | 训练方式<br>Training | WSJ 23 F1 |
| --- | --- | --- |
| Vinyals & Kaiser el al. (2014) [37] | 仅 WSJ，判别式<br>WSJ only, discriminative | 88.3 |
| Petrov et al. (2006) [29] | 仅 WSJ，判别式<br>WSJ only, discriminative | 90.4 |
| Zhu et al. (2013) [40] | 仅 WSJ，判别式<br>WSJ only, discriminative | 90.4 |
| Dyer et al. (2016) [8] | 仅 WSJ，判别式<br>WSJ only, discriminative | 91.7 |
| **Transformer（4 层 / 4 layers）** | 仅 WSJ，判别式<br>WSJ only, discriminative | **91.3** |
| Zhu et al. (2013) [40] | 半监督<br>semi-supervised | 91.3 |
| Huang & Harper (2009) [14] | 半监督<br>semi-supervised | 91.3 |
| McClosky et al. (2006) [26] | 半监督<br>semi-supervised | 92.1 |
| Vinyals & Kaiser el al. (2014) [37] | 半监督<br>semi-supervised | 92.1 |
| **Transformer（4 层 / 4 layers）** | 半监督<br>semi-supervised | **92.7** |
| Luong et al. (2015) [23] | 多任务<br>multi-task | 93.0 |
| Dyer et al. (2016) [8] | 生成式<br>generative | 93.3 |

> Our results in Table 4 show that despite the lack of task-specific tuning our model performs surprisingly well, yielding better results than all previously reported models with the exception of the Recurrent Neural Network Grammar [8].

表 4 的结果表明，尽管没有针对任务专门调优，我们的模型表现仍出奇地好，除循环神经网络语法（Recurrent Neural Network Grammar）[8] 之外，结果优于此前报告的所有模型。

> In contrast to RNN sequence-to-sequence models [37], the Transformer outperforms the Berkeley-Parser [29] even when training only on the WSJ training set of 40K sentences.

与 RNN 序列到序列模型 [37] 相比，即使仅使用 4 万句的 WSJ 训练集进行训练，Transformer 也优于 Berkeley-Parser [29]。

---

## 7 结论 / Conclusion

> In this work, we presented the Transformer, the first sequence transduction model based entirely on attention, replacing the recurrent layers most commonly used in encoder-decoder architectures with multi-headed self-attention.

在本工作中，我们提出了 Transformer——第一个完全基于注意力的序列转导模型，它用多头自注意力取代了编码器-解码器架构中最常用的循环层。

> For translation tasks, the Transformer can be trained significantly faster than architectures based on recurrent or convolutional layers. On both WMT 2014 English-to-German and WMT 2014 English-to-French translation tasks, we achieve a new state of the art. In the former task our best model outperforms even all previously reported ensembles.

对于翻译任务，Transformer 的训练速度可以显著快于基于循环层或卷积层的架构。在 WMT 2014 英德和 WMT 2014 英法翻译任务上，我们都取得了新的最先进水平。在前一个任务中，我们最好的模型甚至超越了此前报告的所有集成模型。

> We are excited about the future of attention-based models and plan to apply them to other tasks. We plan to extend the Transformer to problems involving input and output modalities other than text and to investigate local, restricted attention mechanisms to efficiently handle large inputs and outputs such as images, audio and video. Making generation less sequential is another research goals of ours.

我们对基于注意力的模型的未来感到兴奋，并计划将它们应用于其他任务。我们计划把 Transformer 扩展到涉及文本以外输入输出模态的问题，并研究局部的、受限的注意力机制，以高效处理图像、音频和视频等大规模输入与输出。让生成过程变得不那么依赖顺序，是我们的另一个研究目标。

> The code we used to train and evaluate our models is available at https://github.com/tensorflow/tensor2tensor.

我们用于训练和评估模型的代码可在 https://github.com/tensorflow/tensor2tensor 获取。

---

## 致谢 / Acknowledgements

> We are grateful to Nal Kalchbrenner and Stephan Gouws for their fruitful comments, corrections and inspiration.

我们感谢 Nal Kalchbrenner 和 Stephan Gouws 提出的富有启发的意见、指正与灵感。

---

## 参考文献 / References

> **说明：** 按学术惯例，参考文献条目保留英文原貌，不作逐条翻译（以便读者按原文检索与引用）。文末附有**术语对照表**，可供术语中英对照查阅。

> [1] Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton. Layer normalization. arXiv preprint arXiv:1607.06450, 2016.
> [2] Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. Neural machine translation by jointly learning to align and translate. CoRR, abs/1409.0473, 2014.
> [3] Denny Britz, Anna Goldie, Minh-Thang Luong, and Quoc V. Le. Massive exploration of neural machine translation architectures. CoRR, abs/1703.03906, 2017.
> [4] Jianpeng Cheng, Li Dong, and Mirella Lapata. Long short-term memory-networks for machine reading. arXiv preprint arXiv:1601.06733, 2016.
> [5] Kyunghyun Cho, Bart van Merrienboer, Caglar Gulcehre, Fethi Bougares, Holger Schwenk, and Yoshua Bengio. Learning phrase representations using rnn encoder-decoder for statistical machine translation. CoRR, abs/1406.1078, 2014.
> [6] Francois Chollet. Xception: Deep learning with depthwise separable convolutions. arXiv preprint arXiv:1610.02357, 2016.
> [7] Junyoung Chung, Çaglar Gülçehre, Kyunghyun Cho, and Yoshua Bengio. Empirical evaluation of gated recurrent neural networks on sequence modeling. CoRR, abs/1412.3555, 2014.
> [8] Chris Dyer, Adhiguna Kuncoro, Miguel Ballesteros, and Noah A. Smith. Recurrent neural network grammars. In Proc. of NAACL, 2016.
> [9] Jonas Gehring, Michael Auli, David Grangier, Denis Yarats, and Yann N. Dauphin. Convolutional sequence to sequence learning. arXiv preprint arXiv:1705.03122v2, 2017.
> [10] Alex Graves. Generating sequences with recurrent neural networks. arXiv preprint arXiv:1308.0850, 2013.
> [11] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 770–778, 2016.
> [12] Sepp Hochreiter, Yoshua Bengio, Paolo Frasconi, and Jürgen Schmidhuber. Gradient flow in recurrent nets: the difficulty of learning long-term dependencies, 2001.
> [13] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. Neural computation, 9(8):1735–1780, 1997.
> [14] Zhongqiang Huang and Mary Harper. Self-training PCFG grammars with latent annotations across languages. In Proceedings of the 2009 Conference on Empirical Methods in Natural Language Processing, pages 832–841. ACL, August 2009.
> [15] Rafal Jozefowicz, Oriol Vinyals, Mike Schuster, Noam Shazeer, and Yonghui Wu. Exploring the limits of language modeling. arXiv preprint arXiv:1602.02410, 2016.
> [16] Łukasz Kaiser and Samy Bengio. Can active memory replace attention? In Advances in Neural Information Processing Systems, (NIPS), 2016.
> [17] Łukasz Kaiser and Ilya Sutskever. Neural GPUs learn algorithms. In International Conference on Learning Representations (ICLR), 2016.
> [18] Nal Kalchbrenner, Lasse Espeholt, Karen Simonyan, Aaron van den Oord, Alex Graves, and Koray Kavukcuoglu. Neural machine translation in linear time. arXiv preprint arXiv:1610.10099v2, 2017.
> [19] Yoon Kim, Carl Denton, Luong Hoang, and Alexander M. Rush. Structured attention networks. In International Conference on Learning Representations, 2017.
> [20] Diederik Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In ICLR, 2015.
> [21] Oleksii Kuchaiev and Boris Ginsburg. Factorization tricks for LSTM networks. arXiv preprint arXiv:1703.10722, 2017.
> [22] Zhouhan Lin, Minwei Feng, Cicero Nogueira dos Santos, Mo Yu, Bing Xiang, Bowen Zhou, and Yoshua Bengio. A structured self-attentive sentence embedding. arXiv preprint arXiv:1703.03130, 2017.
> [23] Minh-Thang Luong, Quoc V. Le, Ilya Sutskever, Oriol Vinyals, and Lukasz Kaiser. Multi-task sequence to sequence learning. arXiv preprint arXiv:1511.06114, 2015.
> [24] Minh-Thang Luong, Hieu Pham, and Christopher D Manning. Effective approaches to attention-based neural machine translation. arXiv preprint arXiv:1508.04025, 2015.
> [25] Mitchell P Marcus, Mary Ann Marcinkiewicz, and Beatrice Santorini. Building a large annotated corpus of english: The penn treebank. Computational linguistics, 19(2):313–330, 1993.
> [26] David McClosky, Eugene Charniak, and Mark Johnson. Effective self-training for parsing. In Proceedings of the Human Language Technology Conference of the NAACL, Main Conference, pages 152–159. ACL, June 2006.
> [27] Ankur Parikh, Oscar Täckström, Dipanjan Das, and Jakob Uszkoreit. A decomposable attention model. In Empirical Methods in Natural Language Processing, 2016.
> [28] Romain Paulus, Caiming Xiong, and Richard Socher. A deep reinforced model for abstractive summarization. arXiv preprint arXiv:1705.04304, 2017.
> [29] Slav Petrov, Leon Barrett, Romain Thibaux, and Dan Klein. Learning accurate, compact, and interpretable tree annotation. In Proceedings of the 21st International Conference on Computational Linguistics and 44th Annual Meeting of the ACL, pages 433–440. ACL, July 2006.
> [30] Ofir Press and Lior Wolf. Using the output embedding to improve language models. arXiv preprint arXiv:1608.05859, 2016.
> [31] Rico Sennrich, Barry Haddow, and Alexandra Birch. Neural machine translation of rare words with subword units. arXiv preprint arXiv:1508.07909, 2015.
> [32] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. arXiv preprint arXiv:1701.06538, 2017.
> [33] Nitish Srivastava, Geoffrey E Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan Salakhutdinov. Dropout: a simple way to prevent neural networks from overfitting. Journal of Machine Learning Research, 15(1):1929–1958, 2014.
> [34] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors, Advances in Neural Information Processing Systems 28, pages 2440–2448. Curran Associates, Inc., 2015.
> [35] Ilya Sutskever, Oriol Vinyals, and Quoc VV Le. Sequence to sequence learning with neural networks. In Advances in Neural Information Processing Systems, pages 3104–3112, 2014.
> [36] Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens, and Zbigniew Wojna. Rethinking the inception architecture for computer vision. CoRR, abs/1512.00567, 2015.
> [37] Vinyals & Kaiser, Koo, Petrov, Sutskever, and Hinton. Grammar as a foreign language. In Advances in Neural Information Processing Systems, 2015.
> [38] Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V Le, Mohammad Norouzi, Wolfgang Macherey, Maxim Krikun, Yuan Cao, Qin Gao, Klaus Macherey, et al. Google's neural machine translation system: Bridging the gap between human and machine translation. arXiv preprint arXiv:1609.08144, 2016.
> [39] Jie Zhou, Ying Cao, Xuguang Wang, Peng Li, and Wei Xu. Deep recurrent models with fast-forward connections for neural machine translation. CoRR, abs/1606.04199, 2016.
> [40] Muhua Zhu, Yue Zhang, Wenliang Chen, Min Zhang, and Jingbo Zhu. Fast and accurate shift-reduce constituent parsing. In Proceedings of the 51st Annual Meeting of the ACL (Volume 1: Long Papers), pages 434–443. ACL, August 2013.

---

## 附录：注意力可视化 / Appendix: Attention Visualizations

> **说明：** 原 PDF 的第 13–15 页为附录中的注意力可视化插图（图 3–图 5），图中词汇为英文原文，本对照版将其图形自原 PDF 中导出并以图片形式嵌入，图注中英对照。为便于阅读，插图中所用的英文例句另附中文试译于各图之后。

### 图 3 / Figure 3

![图 3：编码器自注意力中的长距离依赖](/assets/attention/fig3_encoder_self_attention_long_distance.png)

> Figure 3: An example of the attention mechanism following long-distance dependencies in the encoder self-attention in layer 5 of 6. Many of the attention heads attend to a distant dependency of the verb 'making', completing the phrase 'making...more difficult'. Attentions here shown only for the word 'making'. Different colors represent different heads. Best viewed in color.

**图 3：** 编码器自注意力（6 层中的第 5 层）中，注意力机制跟随长距离依赖关系的一个示例。许多注意力头关注动词 "making" 的一个远距离依赖，从而补全短语 "making...more difficult"（使……变得更加困难）。此处仅展示单词 "making" 的注意力。不同颜色代表不同的注意力头。彩色查看效果最佳。

图中所用例句（英文原文与中文试译）：

> It is in this spirit that a majority of American governments have passed new laws since 2009 making the registration or voting process more difficult.

正是本着这种精神，自 2009 年以来，美国大多数州政府通过了新的法律，使选民登记或投票过程变得更加困难。

### 图 4 / Figure 4

![图 4：参与指代消解的两个注意力头](/assets/attention/fig4_anaphora_resolution.png)

> Figure 4: Two attention heads, also in layer 5 of 6, apparently involved in anaphora resolution. Top: Full attentions for head 5. Bottom: Isolated attentions from just the word 'its' for attention heads 5 and 6. Note that the attentions are very sharp for this word.

**图 4：** 同样位于第 5 层（共 6 层）的两个注意力头，显然参与了指代消解。上：头 5 的完整注意力。下：仅来自单词 "its" 的注意力，分别对应注意力头 5 与头 6。注意，该词的注意力非常尖锐（高度集中）。

图中所用例句（英文原文与中文试译）：

> The Law will never be perfect, but its application should be just - this is what we are missing, in my opinion.

法律永远不会完美，但其适用应当公正——在我看来，这正是我们所缺失的东西。

### 图 5 / Figure 5

![图 5：与句子结构相关的注意力头](/assets/attention/fig5_sentence_structure_heads.png)

> Figure 5: Many of the attention heads exhibit behaviour that seems related to the structure of the sentence. We give two such examples above, from two different heads from the encoder self-attention at layer 5 of 6. The heads clearly learned to perform different tasks.

**图 5：** 许多注意力头表现出似乎与句子结构相关的行为。上面给出两个此类示例，它们来自第 5 层（共 6 层）编码器自注意力的两个不同注意力头。这些注意力头显然学会了执行不同的任务。

（图 5 所用例句与图 4 相同：*The Law will never be perfect, but its application should be just - this is what we are missing, in my opinion.*／法律永远不会完美，但其适用应当公正——在我看来，这正是我们所缺失的东西。）

---

## 术语对照表 / Glossary

> 本表汇总正文中的关键术语，按出现顺序大致排列，供对照与检索使用。

| 英文 English | 中文 Chinese | 备注 |
| --- | --- | --- |
| sequence transduction | 序列转导 | 把输入序列映射为输出序列 |
| attention mechanism | 注意力机制 | |
| self-attention / intra-attention | 自注意力 / 内部注意力 | 第 2 节 |
| encoder-decoder structure | 编码器-解码器结构 | |
| recurrence | 循环（结构） | 与 sequential computation 呼应 |
| auto-regressive | 自回归的 | 第 3 节 |
| convolution / kernel | 卷积 / 卷积核 | |
| Transformer | Transformer | 专有架构名，全文保留原文不译 |
| Scaled Dot-Product Attention | 缩放点积注意力 | 3.2.1 |
| additive attention | 加性注意力 | 3.2.1 |
| dot-product (multiplicative) attention | 点积（乘性）注意力 | 3.2.1 |
| compatibility function | 兼容性函数 | 查询与键的匹配度函数 |
| query / key / value | 查询 / 键 / 值 | 3.2 |
| Multi-Head Attention | 多头注意力 | 3.2.2 |
| attention head | 注意力头 | |
| representation subspace | 表示子空间 | 3.2.2 |
| parameter matrix / projection | 参数矩阵 / 投影 | 3.2.2 |
| masked / masking out | 掩蔽 | 3.2.3，置为 −∞ |
| position-wise feed-forward network | 逐位置前馈网络 | 3.3 |
| residual connection | 残差连接 | 3.1 |
| layer normalization | 层归一化 | 3.1 |
| embedding | 嵌入 | 3.4 |
| softmax | softmax | 函数名，保留原文 |
| positional encoding | 位置编码 | 3.5 |
| sinusoid / sinusoidal | 正弦曲线 / 正弦式的 | 3.5 |
| wavelength | 波长 | |
| geometric progression | 等比数列 | |
| extrapolate | 外推 | 3.5 |
| path length | 路径长度 | 第 4 节 |
| long-range dependency | 长程依赖 | 第 4 节 |
| sequential operations | 顺序操作 | 表 1 |
| complexity per layer | 每层复杂度 | 表 1 |
| restricted self-attention | 受限自注意力 | 表 1 |
| dilated convolutions | 空洞卷积 | 第 4 节 |
| separable convolutions | 可分离卷积 | 第 4 节 |
| interpretability | 可解释性 | 第 4 节 |
| attention distribution | 注意力分布 | 第 4 节 |
| byte-pair encoding (BPE) | 字节对编码 | 5.1 |
| word-piece | word-piece（子词单元） | 5.1 |
| token | 词元 | |
| vocabulary | 词表 | |
| sentence pairs | 句子对 | 5.1 |
| batching | 批处理 / 分批 | 5.1 |
| optimizer / Adam | 优化器 / Adam | 5.3 |
| learning rate | 学习率 | 5.3 |
| warmup steps | 预热步数 | 5.3 |
| dropout | dropout（随机失活） | 5.4 |
| residual dropout | 残差 dropout | 5.4 |
| label smoothing | 标签平滑 | 5.4 |
| over-fitting | 过拟合 | 6.2 |
| perplexity (PPL) | 困惑度 | 表 3 |
| BLEU | BLEU | 机器翻译评价指标，保留原文 |
| beam search / beam size | 束搜索 / 束宽 | 6.1 |
| length penalty | 长度惩罚 | 6.1 |
| checkpoint averaging | 检查点平均 | 6.1 |
| ensemble | 集成（模型） | 表 2 |
| state of the art | 最先进水平 | |
| development set | 开发集 | |
| FLOPs | 浮点运算次数 | 表 2 |
| constituency parsing | 成分句法分析 | 6.3 |
| Penn Treebank / WSJ | 宾州树库 / 《华尔街日报》 | 6.3 |
| semi-supervised | 半监督 | 6.3 |
| discriminative / generative | 判别式 / 生成式 | 表 4 |
| multi-task | 多任务 | 表 4 |
| anaphora resolution | 指代消解 | 图 4 |

---

## 译注 / Translator's Notes

1. **保留原文的术语：** `Transformer`、`softmax`、`dropout`、`BLEU`、`word-piece`、`base`／`big`（模型规模版本）等在中文学术界习惯直接使用英文，故全文保留原文，不强行翻译。
2. **公式记法：** 为兼容各类 Markdown 阅读器，公式以 Unicode 纯文本表示：`^` 表示上标（如 `QK^T`），`_` 表示下标（如 `d_k`），`R^(d_model×d_k)` 表示实数矩阵空间 R^{d_model×d_k}，`Σ_{i=1}^{d_k}` 表示求和。
3. **原文自身的笔误：** 原文 6.1 节正文称英法任务上 big 模型 BLEU 为 41.0，而表 2 中该值为 41.8；摘要中亦为 41.8。本对照版按原 PDF 原样保留，未作改动，特此说明。
4. **表格空白：** 原表 1–表 4 中留空的单元格表示"未列出（与 base 模型相同）"或"不适用"，本对照版保留其空白形态。
5. **页眉与页码：** 原 PDF 的页眉（标题、作者）与页码未逐页复制；正文内容完整对应原 PDF 第 1–15 页。

---

*本对照版依据工作区内的 `注意力.pdf`（arXiv:1706.03762v7）逐段翻译整理；英文原文均引自该 PDF，未作删改。插图由原 PDF 导出，存放于 `/assets/attention/`。*
