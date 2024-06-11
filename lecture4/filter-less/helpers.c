#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, and blue
            int average =
                round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);

            // Update pixel values
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            float originalRed = image[i][j].rgbtRed;
            float originalGreen = image[i][j].rgbtGreen;
            float originalBlue = image[i][j].rgbtBlue;

            int sepiaRed = round(
                fminf(.393 * originalRed + .769 * originalGreen + .189 * originalBlue, 255.0));
            int sepiaGreen = round(
                fminf(.349 * originalRed + .686 * originalGreen + .168 * originalBlue, 255.0));
            int sepiaBlue = round(
                fminf(.272 * originalRed + .534 * originalGreen + .131 * originalBlue, 255.0));

            // Update pixel with sepia values
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, w = width, n = round(w / 2.0); j < n; j++)
        {
            // Swap pixels
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
}

// Blur pixel helper function
RGBTRIPLE blur_pixel(int i, int j, int height, int width, RGBTRIPLE image[height][width])
{
    int red = 0;
    int green = 0;
    int blue = 0;
    int counter = 0;

    for (int h = i - 1; h <= i + 1; h++)
    {
        for (int w = j - 1; w <= j + 1; w++)
        {
            if (h >= 0 && h < height && w >= 0 && w < width)
            {
                red += image[h][w].rgbtRed;
                green += image[h][w].rgbtGreen;
                blue += image[h][w].rgbtBlue;
                counter++;
            }
        }
    }

    RGBTRIPLE blurred_pixel;
    blurred_pixel.rgbtRed = round((float) red / counter);
    blurred_pixel.rgbtGreen = round((float) green / counter);
    blurred_pixel.rgbtBlue = round((float) blue / counter);

    return blurred_pixel;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // Apply blur to each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = blur_pixel(i, j, height, width, copy);
        }
    }
}
