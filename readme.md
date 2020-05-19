The idea is that you can use this to search through a dataset of images to find duplicates.
For example, too many duplicates can cause overfitting in machine learning models.

Unfortunately, it's a pretty slow O(n) linear search. That's because every image in the index
needs to calculate a unique chi-squared distance from an uploaded image, so this obviously can't be sorted.
But doing this allows returning a list of similar images.

![alt text](https://raw.githubusercontent.com/tjbergstrom/Reverse-Image-Search/master/Reverse%20Image%20Search/screenshot.png)

