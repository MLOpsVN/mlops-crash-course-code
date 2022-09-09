# Model validation: The model is confirmed to be adequate for deployment—that its predictive performance is better than a certain baseline. This step occurs after you successfully train the model given the new data. You evaluate and validate the model before it's promoted to production. This offline model validation step consists of the following.

# Producing evaluation metric values using the trained model on a test dataset to assess the model's predictive quality.

# Comparing the evaluation metric values produced by your newly trained model to the current model, for example, production model, baseline model, or other business-requirement models. You make sure that the new model produces better performance than the current model before promoting it to production.

# Making sure that the performance of the model is consistent on various segments of the data. For example, your newly trained customer churn model might produce an overall better predictive accuracy compared to the previous model, but the accuracy values per customer region might have large variance.
# Making sure that you test your model for deployment, including infrastructure compatibility and consistency with the prediction service API.
