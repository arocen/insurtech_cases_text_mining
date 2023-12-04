# Text mining of insurtech cases from China Banking and Insurance News.

## Model
### BERTopic
- [x] Enable 2-grams, 3-grams and rerun BERTopic.
- [x] Enable loading dictionary and rerun jieba
- [ ] Assign topic names to model.

## Visualization
### topicwizard
- [x] Check if the order of corpus passed to topicwizard is the same to that passed to BERTopic. (Add sort() to path list of txt files. Ensure the parent folder of txt files are same to BERTopic and topicwizard.)
- [x] Use corpus after cutting words? Or just use raw corpus? (A: Use cut corpus.)
- [ ] Make wordcloud font more clear.
- [ ] Assign titles to documents in documents panel.