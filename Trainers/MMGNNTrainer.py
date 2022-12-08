import torch
import torch.backends.cudnn as cudnn

from Trainers.BaseTrainer import BaseTrainer
from Models.Encoder import ImageEncoder,TextEncoder,ProjectionHead
from Models.GCN import GCN,GCNClassifier

PROJECTION_DIM = 256

class CLIPGNNTrainer(BaseTrainer):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.build_model()
        self.getTrainableParams()
        self.setup_optimizer_losses()


    def build_model(self):
        # Model
        print('==> Building model..')
        self.models['image_encoder'] = ImageEncoder().to(self.device)
        self.models['text_encoder'] = TextEncoder().to(self.device)
        self.models['image_projection'] = ProjectionHead(2048,PROJECTION_DIM).to(self.device)
        self.models['text_projection'] = ProjectionHead(768,PROJECTION_DIM).to(self.device)
        self.models['graph'] = GCNClassifier(PROJECTION_DIM,2).to(self.device)
        if self.device in ['cuda','mps']:
            for key, model in self.models.items():
                self.models[key] = torch.nn.DataParallel(model)
                cudnn.benchmark = True

    def train_epoch(self,epoch):
        self.setTrain()
        train_loss = 0
        correct = 0
        total = 0
        for image, text, label in self.train_loader:
            padded_text, attention_masks, labels = padded_text.to(self.device), attention_masks.to(self.device), labels.to(self.device)
            
            self.optimizer.zero_grad()
            
            outputs = self.net(padded_text, attention_masks)
            loss = self.criterion(outputs, labels)
            loss.backward()
            

            self.optimizer.step()
            
            # Metrics Calculation
            train_loss += loss.item()
            total += labels.size(0)

            _, predicted = outputs.max(1)
            correct += predicted.eq(labels).sum().item()
    
        acc = 100.*correct/total
            
        print("Backdoor Training --- Epoch : {} | Accuracy : {} | Loss : {}".format(epoch,acc,train_loss/total))    