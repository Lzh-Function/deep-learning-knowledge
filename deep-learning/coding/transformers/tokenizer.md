## これは何
transformersのTokenizerについて理解したい

## まずは概要
TransformersにおけるTokenizer（トークナイザー）は、人間が理解する「自然言語（テキスト）」と、モデルが理解する「数値（テンソル）」の間を取り持つ**翻訳機**の役割を果たしています。

モデル内部で「何が起きているのか」を理解するために、Tokenizerの処理フローを4つのステップに分解して詳細に解説します。

-----

### Tokenizerの全体像：4つのパイプライン

Tokenizerにテキストを与えると、内部では主に以下の順序で処理が行われます。

1.  **Normalization** (正規化)
2.  **Pre-tokenization** (事前分割)
3.  **Model** (サブワード分割)
4.  **Post-processor** (後処理)

それぞれの工程で何が起きているかを見ていきましょう。

#### 1\. Normalization (正規化)

テキストをきれいに整える工程です。

  * **何をするか:** 大文字・小文字の統一（Lowercasing）、Unicode正規化（全角・半角の統一など）、アクセント記号の削除など。
  * **例:**
      * 入力: `HéLLo World!`
      * 出力: `hello world!` (BERTのuncasedモデルなどの場合)

#### 2\. Pre-tokenization (事前分割)

テキストを「単語」のような単位にざっくりと分割します。

  * **何をするか:** 空白（スペース）や句読点で分割します。ここでの分割は、次のステップ（サブワード分割）のベースになります。
  * **例:**
      * 入力: `hello world!`
      * 出力: `['hello', 'world', '!']`

#### 3\. Model (サブワード分割 - 最も重要)

ここがTokenizerの核心部分です。**「未知語（Out-of-Vocabulary）」をなくすため**に、単語をさらに細かい意味のある単位（サブワード）に分割します。

  * **なぜこれが必要か:**
      * 世界中のすべての単語を辞書に登録するのは不可能です。
      * そこで、「頻出する単語」はそのまま登録し、「珍しい単語」は「よく見る部分文字列」の組み合わせとして表現します。
  * **アルゴリズムの例:**
      * **WordPiece (BERT等):** 単語の途中を表すサブワードに `##` をつけます。
          * 例: `tokenization` -\> `['token', '##ization']`
      * **BPE (GPT-2, RoBERTa等):** 特定の文字ペアを結合していきます。
          * 例: `tokenization` -\> `['token', 'ization']` (スペース情報が含まれる場合も)
      * **SentencePiece (T5, ALBERT等):** 空白も含めて1つの文字として扱い、生のテキストを直接処理します。
  * **例:**
      * 入力: `['unhappiness']`
      * 出力: `['un', '##happi', '##ness']` (WordPieceの場合)

#### 4\. Post-processor (後処理)

モデルに入力するための最終的な整形を行います。

  * **何をするか:**
      * **Special Tokensの付与:** 文頭の `[CLS]`、文の区切りの `[SEP]` などを追加します。
      * **IDへの変換:** 各トークンを、辞書（Vocabulary）に基づいて整数（ID）に変換します。
  * **例:**
      * 入力: `['hello', 'world', '!']`
      * 出力 (Tokens): `['[CLS]', 'hello', 'world', '!', '[SEP]']`
      * 出力 (IDs): `[101, 7592, 2088, 999, 102]`

-----

### 入力と出力の詳細

ユーザーがコードで何を与え、何を受け取るかを確認します。

#### 1\. 何を与えるべきか？ (Input)

基本的には「文字列」または「文字列のリスト」を与えます。

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

text = "I am learning Transformers."
# 基本的な呼び出し
encoded = tokenizer(
    text,
    padding=True,       # バッチ内で長さを揃える（0埋め）
    truncation=True,    # 最大長を超えたら切り捨てる
    max_length=10,      # 最大長の指定
    return_tensors="pt" # PyTorchのTensorで返す ("np", "tf" も可)
)
```

#### 2\. 何が返ってくるか？ (Output)

Tokenizerは通常、辞書形式（dict-like object）を返します。以下の3つのキーが重要です。

| キー | 名前 | 内容 | 役割 |
| :--- | :--- | :--- | :--- |
| `input_ids` | トークンID | `[101, 1045, 2572, ...]` | 単語を数値化したもの。Embedding層に入力される。 |
| `token_type_ids` | セグメントID | `[0, 0, 0, ...]` | 2つの文を入力した際、どちらの文に属するか（0か1か）を区別する。BERTなどで使用。 |
| `attention_mask` | アテンションマスク | `[1, 1, 1, 0, 0]` | 1は「意味のある単語」、0は「パディング（無視すべき部分）」。Attention機構が0の部分を見ないようにする。 |

-----

### 日本語モデルの場合の特記事項

英語はスペースで単語が区切られていますが、日本語にはスペースがありません。そのため、Hugging Faceの日本語モデルを使用する場合、ステップ2（Pre-tokenization）の部分で **「形態素解析器（MeCabやSudachi）」** が内部で動くことが多いです。

  * **東北大学のBERT (`cl-tohoku/bert-base-japanese`)**
      * 内部で `MeCab` を使用して単語分割を行い、その後 WordPiece でサブワード化しています。
      * そのため、実行環境に `mecab` ライブラリのインストールが必要になることがあります。

### まとめ

Tokenizerの中では、単に辞書を引いているだけではなく、**「テキストの正規化 -\> 文法的な分割 -\> 統計的なサブワード分割 -\> 特殊トークンの付与」** という一連の高度な処理が行われています。

これにより、モデルは「未知語」に遭遇しても、「知っているサブワードの組み合わせ」として意味を推測して処理を続行できるのです。

## 自然言語ではなく、決まったトークンとトークナイズを行うカスタムの場合は？
データが「1文単位」であり、かつ「独自のトークナイズ・アルゴリズム」を使いたい場合、既存のモデル（BERTなど）のトークナイザーを無理に使う必要はありません。

この場合、**`transformers.PreTrainedTokenizer` を継承して、独自のトークナイザークラスを作成する** のが最も行儀の良い（Hugging Faceのエコシステムに乗る）方法です。

これにより、自作のアルゴリズムを使いつつ、`Trainer` や `DataCollator` といったHugging Faceの便利な機能をそのまま利用できます。

### 実装ステップ

カスタムトークナイザーを作るには、以下のメソッドを実装したクラスを作成します。

1.  **`_tokenize`**: テキストをトークン（文字列）のリストに分割するロジック。
2.  **`_convert_token_to_id`**: トークン（文字列）をID（整数）に変換する。
3.  **`_convert_id_to_token`**: ID（整数）をトークン（文字列）に戻す。
4.  **`vocab_size`**: 語彙数を返すプロパティ。
5.  **`save_vocabulary`**: 語彙ファイルを保存するロジック（`save_pretrained`用）。

-----

### 実装コード例

ここでは例として、「スペースで分割するだけ」という非常に単純なカスタムアルゴリズムを想定しますが、`_tokenize` の中身をあなたの好きなアルゴリズム（正規表現や辞書マッチングなど）に書き換えれば、どんなロジックでも動きます。

```python
import json
import os
from typing import List, Optional
from transformers import PreTrainedTokenizer

class MyCustomTokenizer(PreTrainedTokenizer):
    def __init__(
        self,
        vocab_file: str = None,
        unk_token="[UNK]",
        sep_token="[SEP]",
        pad_token="[PAD]",
        cls_token="[CLS]",
        mask_token="[MASK]",
        **kwargs
    ):
        """
        初期化: 語彙辞書(vocab)を読み込む
        """
        self.vocab = {}
        self.ids_to_tokens = {}
        
        # 語彙ファイルの読み込み（JSON形式を想定）
        if vocab_file and os.path.exists(vocab_file):
            with open(vocab_file, "r", encoding="utf-8") as f:
                self.vocab = json.load(f)
            self.ids_to_tokens = {v: k for k, v in self.vocab.items()}
        
        # 親クラスの初期化（特殊トークンの設定など）
        super().__init__(
            unk_token=unk_token,
            sep_token=sep_token,
            pad_token=pad_token,
            cls_token=cls_token,
            mask_token=mask_token,
            **kwargs
        )

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    def get_vocab(self):
        return self.vocab

    def _tokenize(self, text: str) -> List[str]:
        """
        【重要】ここに独自の分割アルゴリズムを書く
        例: 単純なスペース分割 + 小文字化
        """
        return text.lower().split()

    def _convert_token_to_id(self, token: str) -> int:
        """
        トークン(str) -> ID(int)
        辞書になければ unk_token_id を返す
        """
        return self.vocab.get(token, self.unk_token_id)

    def _convert_id_to_token(self, index: int) -> str:
        """
        ID(int) -> トークン(str)
        """
        return self.ids_to_tokens.get(index, self.unk_token)

    def save_vocabulary(self, save_directory: str, filename_prefix: Optional[str] = None):
        """
        save_pretrained() を呼んだ時に実行される保存ロジック
        """
        if not os.path.isdir(save_directory):
            os.makedirs(save_directory)
            
        vocab_file = os.path.join(
            save_directory, (filename_prefix + "-" if filename_prefix else "") + "vocab.json"
        )
        
        with open(vocab_file, "w", encoding="utf-8") as f:
            json.dump(self.vocab, f, ensure_ascii=False)
            
        return (vocab_file,)
```

-----

### 利用フロー

#### 1\. 語彙（Vocab）の準備

まず、あなたのデータセットに出現する単語のリスト（辞書）を作る必要があります。ID `0`, `1`... などに特殊トークンを割り当てておくのが一般的です。

```python
# 語彙辞書の作成例（実際は全データからスキャンして作成する）
my_vocab = {
    "[PAD]": 0, "[UNK]": 1, "[CLS]": 2, "[SEP]": 3, "[MASK]": 4,
    "this": 5, "is": 6, "a": 7, "pen": 8, "custom": 9, "data": 10
    # ... 他の単語 ...
}

# 一旦ファイルに保存
with open("my_vocab.json", "w") as f:
    json.dump(my_vocab, f)
```

#### 2\. トークナイザーのロードと使用

作成したクラスをインスタンス化します。

```python
# インスタンス化
tokenizer = MyCustomTokenizer(vocab_file="my_vocab.json")

# テストデータ
text = "This is a custom data"

# 実行
encoded = tokenizer(text)

print("Tokens:", tokenizer.convert_ids_to_tokens(encoded["input_ids"]))
print("IDs:   ", encoded["input_ids"])

# 出力例:
# Tokens: ['[CLS]', 'this', 'is', 'a', 'custom', 'data', '[SEP]']
# IDs:    [2, 5, 6, 7, 9, 10, 3]
```

**解説:**

  * `_tokenize` は `"this", "is", ...` を返しますが、親クラスの `tokenizer()` メソッドが自動的に `[CLS]` (ID:2) と `[SEP]` (ID:3) を付与してくれます。これは継承の大きなメリットです。
  * パディングやTruncation（切り詰め）などの引数もそのまま使えます。

#### 3\. モデル・Trainerへの統合

この `tokenizer` オブジェクトを、前回紹介した `CustomDataset` や `Trainer` にそのまま渡すことができます。

```python
# モデルのConfigには、このTokenizerのvocab_sizeを渡す
config = SimpleCustomConfig(vocab_size=tokenizer.vocab_size, ...)
model = SimpleCustomModel(config)

# Trainerは tokenizer.pad_token_id などを参照してバッチ処理を行う
trainer = Trainer(
    model=model,
    tokenizer=tokenizer, # ここで渡すことで、保存時に一緒に保存される
    ...
)
```

### まとめ

  * **継承元:** `transformers.PreTrainedTokenizer`
  * **必須実装:**
      * `_tokenize(text)`: ここにあなたの**カスタムアルゴリズム**を書きます。
      * `_convert_token_to_id`: 辞書引き。
      * `vocab_size`: 辞書サイズ。
  * **メリット:**
      * Hugging Faceの標準機能（`[CLS]`付与、Padding、Trainer連携、save\_pretrained）がすべてそのまま使えます。
      * 「1データ＝1文」であっても、バッチ化の際のパディング処理などはライブラリに任せたほうが楽です。

あなたの想定している「カスタムのアルゴリズム」がどのようなルール（正規表現、特定の文字単位、外部ライブラリ利用など）か教えていただければ、`_tokenize` メソッドの実装例をさらに具体的に提示できます。いかがいたしましょうか？