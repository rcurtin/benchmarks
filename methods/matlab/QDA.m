% @file QDA.m
%
% QDA with matlab.
% Requires Statistics and Machine Learning toolbox installed.
function qda(cmd)
% This program trains the QDA on the given labeled
% training set and then uses the trained classifier to classify the points
% in the given test set. Labels are expected to be the last row of the
% training set.
%
% Required options:
%     (-T) [string]    A file containing the test set.
%     (-t) [string]    A file containing the training set.

trainFile = regexp(cmd, '.*?-t ([^\s]+)', 'tokens', 'once');
testFile = regexp(cmd, '.*?-T ([^\s]+)', 'tokens', 'once'); 

% Load input dataset.
TrainData = csvread(trainFile{:});
TestData = csvread(testFile{:});

% Use the last row of the training data as the labels.
labels = TrainData(:,end);
% Remove the label row.
TrainData = TrainData(:,1:end-1);

% Create and train the classifier.
total_time = tic;
classifier = fitcdiscr(TrainData, labels, 'DiscrimType', 'quadratic');
% Run Classifier on the test dataset.
labels = predict(classifier, TestData);
disp(sprintf('[INFO ]   total_time: %fs', toc(total_time)))

% Save prediction of each class for test data.
csvwrite('predictions.csv', labels);

end
