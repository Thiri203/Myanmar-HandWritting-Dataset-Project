# Myanmar Handwriting Dataset Training Report

## Objective

The goal of this experiment is to compare CNN training behavior across three versions of the Myanmar handwriting dataset: single, stroke, and time. For each dataset, I trained the same CNN setup with 20, 50, 100, and 200 classes. The main purpose is not only to report the final accuracy, but also to observe how training changes when the dataset type and number of classes change.

## Experimental Setup

All experiments used a simple CNN classifier with grayscale 64 x 64 input images. The batch size was 64, the learning rate was 0.001, and the maximum number of epochs was 10. Early stopping was used with patience 3. For validation, one sample per class was used, so the validation set size is the same as the number of classes. Because the validation set is small, the accuracy values should be interpreted carefully: for example, with 20 classes, one correct validation sample already equals 5% accuracy.

## Result Summary

| Dataset | Classes | Chance Acc | Best Val Acc | Epochs | Validation Loss | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| single | 20 | 0.0500 | 0.0500 | 4 | 2.9255 | Chance level |
| single | 50 | 0.0200 | 0.3600 | 10 | 2.7617 | Meaningful learning |
| single | 100 | 0.0100 | 0.0100 | 4 | 4.6005 | Chance level |
| single | 200 | 0.0050 | 0.0050 | 4 | 5.2948 | Chance level |
| stroke | 20 | 0.0500 | 0.0500 | 4 | 2.9989 | Chance level |
| stroke | 50 | 0.0200 | 0.0200 | 4 | 3.9154 | Chance level |
| stroke | 100 | 0.0100 | 0.0200 | 6 | 4.6057 | Slightly above chance |
| stroke | 200 | 0.0050 | 0.0050 | 4 | 5.2990 | Chance level |
| time | 20 | 0.0500 | 0.0500 | 4 | 2.9961 | Chance level |
| time | 50 | 0.0200 | 0.0200 | 4 | 3.9142 | Chance level |
| time | 100 | 0.0100 | 0.0100 | 4 | 4.6055 | Chance level |
| time | 200 | 0.0050 | 0.0050 | 4 | 5.2989 | Chance level |

## Single Dataset Training

The single dataset gave the best result among the three datasets, especially in the 50-class experiment. With 20 classes, the validation accuracy stayed at 0.05, which is exactly chance level. Even though training accuracy increased from 0.0244 to 0.0976, the model did not generalize on the validation set.

For 50 classes, the training improved clearly. Validation accuracy increased from 0.02 to 0.36, and validation loss decreased from about 3.91 to 2.76. This is the strongest result in the whole experiment. It shows that the single image representation is easier for the CNN to learn, at least when the number of classes is not too high.

For 100 and 200 classes, the model returned to chance-level behavior. The 100-class run stopped at 0.01 accuracy, and the 200-class run stopped at 0.005 accuracy. This suggests that the current model and data split are not enough for larger class counts. The class count grows faster than the amount of useful training data, so the model cannot separate many Myanmar syllable classes reliably.

## Stroke Dataset Training

The stroke dataset was harder than the single dataset. For 20 classes, the result stayed at chance level, with best validation accuracy of 0.05. For 50 classes, the model also stayed at chance level, with best validation accuracy of 0.02.

The only stroke run that showed any improvement was the 100-class experiment. It reached 0.02 validation accuracy while chance accuracy was 0.01. This is technically above chance, but still very weak. It means the model learned a small signal, but not enough to make useful predictions. For 200 classes, the model again stayed at 0.005 validation accuracy, which is chance level.

Overall, the stroke dataset did not train well with the current CNN setup. One possible reason is that stroke images may contain more fragmented or sparse visual information. If the stroke representation is not visually consistent between samples, the CNN has difficulty learning stable features.

## Time Dataset Training

The time dataset had the weakest overall performance. All four class settings stayed at chance level: 0.05 for 20 classes, 0.02 for 50 classes, 0.01 for 100 classes, and 0.005 for 200 classes. The losses were also close to the expected random-classification losses for each class count.

The time dataset may include temporal writing information converted into image form, but the current CNN treats the input only as a static image. Because of that, the model may not be using the most important information in the time-based data. A sequence model or a model that directly uses the temporal stroke order may be more suitable than this simple CNN.

## Cross-Dataset Comparison

Across the three datasets, the single dataset was the easiest for the CNN to train. It produced the only clearly meaningful result: 36% validation accuracy on 50 classes. The stroke dataset was more difficult and only showed a very small above-chance signal at 100 classes. The time dataset did not show meaningful learning in any class setting.

Increasing the number of classes made training much harder. In all datasets, the 200-class result stayed at chance level. This shows that the current model, current amount of data, and current validation split are not strong enough for large-scale Myanmar syllable classification. The model often predicts only a few labels correctly, while most validation classes remain wrong.

The results also show that the representation of the handwriting matters. A normal single image is easier for a CNN because the full character shape is directly visible. Stroke and time versions may contain useful information, but the current model does not extract it well. They may need a different preprocessing method, stronger augmentation, or an architecture designed for stroke/time sequence information.

## Final Conclusion

From these experiments, the CNN learns best on the single dataset and struggles on the stroke and time datasets. The best result is from the single dataset with 50 classes, where validation accuracy reached 0.36 compared with 0.02 chance accuracy. This shows real learning. However, most other runs stayed at chance level, especially when the class count increased to 100 or 200.

My conclusion is that the current training setup is only a starting baseline. It can learn some useful features from the single dataset, but it is not strong enough for larger class counts or for stroke/time representations. To improve the project, I should collect more samples per class (which we can combine our classmate dataset), use stronger augmentation, tune the CNN architecture, and consider sequence-based models for stroke and time data.

## Main Dataset Limits

Only one main writer folder is currently used.
Each class has very few samples, usually around 3 to 5.
Validation accuracy is unstable because one class has only one validation image.
Myanmar syllables have many visually similar classes.
Stroke and time data may need sequence models, not just image CNNs.
4,413 total possible syllables is large, but the collected sample count per syllable is too small for strong large-class training.

## Future Training Direction I could Do More

Collect more writers and more samples per syllable.
Use data augmentation: rotation, shift, scale, thickness changes.
Use transfer learning or stronger CNNs.
Try sequence models for raw stroke data:
RNN/LSTM/GRU
Transformer
1D CNN over stroke coordinates

