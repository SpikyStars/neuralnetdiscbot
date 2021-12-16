import torchvision.models as models
import torchvision.transforms as transforms
import torch

k_results = 5

model = models.resnet50(pretrained=True)
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
preprocess = transforms.Compose(
    [transforms.Resize(256),
     transforms.CenterCrop(224),
     transforms.ToTensor(),
     normalize]
)

# should be fine to keep it in evaluation mode, since it is a pre-trained model
model.eval()
print("ResNet50 loaded!")

classes = open("data/imagenet_classes.txt").read().splitlines()
print("ImageNet classes loaded!")


def classify_image(img):
    # autograd turned off for performance - unneeded in evaluation
    with torch.no_grad():
        # pass appropriate image batches to the model
        batch = torch.unsqueeze(preprocess(img), 0)
        out = model(batch)
        scaled_out = torch.nn.functional.softmax(out, dim=1)
        values, indices = torch.topk(scaled_out, k_results)
        return format_results(values, indices)


def format_results(values, indices):
    rounding = 2
    results = []
    # indices[0] holds the class labels index, values[0] holds the confidence
    for ranking, label_idx in enumerate(indices[0]):
        label_str = classes[label_idx]
        percent = values[0][ranking].item() * 100
        percent_round = round(percent, rounding)
        results.append((label_str, percent_round))
    return results

