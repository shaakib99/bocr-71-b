class Recognizer:
  def __init__(self,
               weights = '',
               image = '',
               img_size = 640,
               conf_thres = 0.25,
               iou_thres = 0.45,
               device = '',
               view_img = False,
               save_txt = False,
               save_conf = False,
               classes = None,
               agnostic_nms = True,
               augment = True,
               update = True,
               project = 'runs/detect',
               name = 'exp',
               exist_ok = True):
    self.weights = weights
    self.source = image
    self.img_size = img_size
    self.conf_thres = conf_thres
    self.iou_thres = iou_thres
    self.device = device
    self.view_img = view_img
    self.save_txt = save_txt
    self.save_conf = save_conf
    self.classes = classes
    self.agnostic_nms = agnostic_nms
    self.augment = augment
    self.update = update
    self.project = project
    self.name = name
    self.exist_ok = exist_ok