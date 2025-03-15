import torch
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from torch import nn, optim
import timm


class PlayingCardDataset(Dataset):
    """
    Running example pytorch tutorial from
    https://youtu.be/tHL5STNJKag?si=PWJoGxT1Vr5X6GMP
    """

    def __init__(self, data_dir, transform=None):
        self.data = datasets.ImageFolder(data_dir, transform=transform)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    @property
    def classes(self):
        return self.data.classes


def setup_dataloader_for_batch():
    # show getting image by index
    dataset = PlayingCardDataset(data_dir="input/cards-images-dataset/train")
    len(dataset)
    image, label = dataset[0]

    # list out the label to card
    data_dir = "input/cards-images-dataset/train"
    target_to_class = {v: k for k, v in datasets.ImageFolder(data_dir).class_to_idx.items()}
    print(target_to_class)

    # transofmr to all same size
    transform = transforms.Compose(
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
    )
    data_dir = "input/cards-images-dataset/train"
    dataset = PlayingCardDataset(data_dir)
    image, label = dataset[100]
    print(image.shape)

    # batching dataset into dataloader for model
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    for images, labels in dataloader:
        break
    return dataloader, transform


class SimpleCardClassifier(nn.Module):
    def __init__(self, num_classes=53):
        super(SimpleCardClassifier, self).__init__()
        self.base_model = timm.create_model("efficientnet_b0", pretrained=True)

        self.features = nn.Sequential(*list(self.base_model.children())[:-1])

        enet_out_size = 1280
        self.classifier = nn.Linear(enet_out_size, num_classes)

    def forward(self, x):
        x = self.features(x)
        output = self.classifier(x)
        return output


if __name__ == "__main__":
    # setup dataloader for batch
    dataloader, transform = setup_dataloader_for_batch()

    # create model
    model = SimpleCardClassifier(num_classes=53)
    print(str(model)[:500])
    example_out = model(dataloader.images)
    print(example_out.shape)

    # training loop
    ## Loss function
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    for images, labels in dataloader:
        criterion(example_out, labels)

    train_folder = "foo/train"
    valid_folder = "foo/valid"
    test_folder = "foot/test"
    train_dataset = PlayingCardDataset(train_folder, transform=transform)
    val_dataset = PlayingCardDataset(valid_folder, transform=transform)
    test_dataset = PlayingCardDataset(test_folder, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    num_epoch = 5
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    train_losses, val_losses = [], []
    model = SimpleCardClassifier(num_classes=53)
    model.to(device)
    for epoch in range(num_epoch):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * images.size(0)
    train_loss = running_loss / len(train_loader.dataset)
    train_losses.append(train_loss)

    # validation
    model.eval()
    running_loss = 0.0
    with torch.no_grad():
        for images, labels in val_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)
            running_loss += loss.item() * images.size(0)
    val_loss = running_loss / len(val_loader.dataset)
    val_losses.append(val_loss)

    # print epoch stats
    print(f"Epoch {epoch}/{num_epoch} - Train loss: {train_loss}, Validaation: {val_loss}")
