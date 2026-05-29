import torch
import torch.nn as nn


class TextCNN(nn.Module):
    def __init__(
        self,
        vocabSize: int,
        embedDim: int,
        numClasses: int,
        dropout: float = 0.5,
    ):
        super().__init__()

        self.embedding = nn.Embedding(vocabSize, embedDim)

        self.conv3 = nn.Conv1d(embedDim, 128, kernel_size=3)
        self.conv4 = nn.Conv1d(embedDim, 128, kernel_size=4)
        self.conv5 = nn.Conv1d(embedDim, 128, kernel_size=5)

        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(128 * 3, numClasses)

    def convBlock(self, x, conv):
        x = conv(x)
        x = torch.relu(x)
        x = torch.max(x, dim=2)[0]
        return x

    def forward(self, x):
        x = self.embedding(x)
        x = x.permute(0, 2, 1)

        x3 = self.convBlock(x, self.conv3)
        x4 = self.convBlock(x, self.conv4)
        x5 = self.convBlock(x, self.conv5)

        x = torch.cat([x3, x4, x5], dim=1)
        x = self.dropout(x)

        return self.fc(x)