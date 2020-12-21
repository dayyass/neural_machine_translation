import sentencepiece as spm
from torch.utils.data import Dataset
from tqdm import tqdm


def load_data(
    data_path: str,
    tokenizer: spm.SentencePieceProcessor,
    add_bos: bool = False,
    add_eos: bool = False,
    verbose: bool = True,
):
    """
    Load data and apply tokenizer to each sentence.
    """

    data_list = []
    with open(data_path) as fp:
        if verbose:
            fp = tqdm(fp)  # add tqdm
        for line in fp:
            data_list.append(
                tokenizer.encode(line, add_bos=add_bos, add_eos=add_eos),  # tokenize
            )
    return data_list


class WMTDataset(Dataset):
    """
    WMT Dataset with tokenized sentences.
    """

    def __init__(
        self,
        from_lang_data_path: str,
        to_lang_data_path: str,
        from_lang_tokenizer_path: str,
        to_lang_tokenizer_path: str,
        verbose: bool = True,
    ):
        self.from_lang_data_path = from_lang_data_path
        self.to_lang_data_path = to_lang_data_path
        self.from_lang_tokenizer_path = from_lang_tokenizer_path
        self.to_lang_tokenizer_path = to_lang_tokenizer_path

        # load tokenizers
        self.from_lang_tokenizer = spm.SentencePieceProcessor(
            model_file=self.from_lang_tokenizer_path,
        )
        self.to_lang_tokenizer = spm.SentencePieceProcessor(
            model_file=self.to_lang_tokenizer_path,
        )

        # load "from" language
        self.from_lang_list = load_data(
            data_path=self.from_lang_data_path,
            tokenizer=self.from_lang_tokenizer,
            add_bos=False,
            add_eos=False,
            verbose=verbose,
        )

        # load "to" language
        self.to_lang_list = load_data(
            data_path=self.to_lang_data_path,
            tokenizer=self.to_lang_tokenizer,
            add_bos=True,
            add_eos=True,
            verbose=verbose,
        )

    def __len__(self):
        assert len(self.from_lang_list) == len(self.to_lang_list)

        return len(self.from_lang_list)

    def __getitem__(self, idx):
        return self.from_lang_list[idx], self.to_lang_list[idx]
