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

// Define the Sobel kernels for Gx and Gy
int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};

int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

// Compute the edge-detected value for a pixel using the Sobel operator
RGBTRIPLE compute_edge_pixel(int i, int j, int height, int width, RGBTRIPLE image[height][width])
{
    // Initialize Gx and Gy for each color channel
    int Gx_r = 0, Gx_g = 0, Gx_b = 0;
    int Gy_r = 0, Gy_g = 0, Gy_b = 0;

    // Iterate over the 3x3 grid surrounding the pixel
    for (int di = -1; di <= 1; di++)
    {
        for (int dj = -1; dj <= 1; dj++)
        {
            int ni = i + di;
            int nj = j + dj;

            // Check if the neighboring pixel is within bounds
            if (ni >= 0 && ni < height && nj >= 0 && nj < width)
            {
                // Get the RGB values of the neighboring pixel
                int r = image[ni][nj].rgbtRed;
                int g = image[ni][nj].rgbtGreen;
                int b = image[ni][nj].rgbtBlue;

                // Update Gx and Gy for each color channel
                Gx_r += r * Gx[di + 1][dj + 1];
                Gx_g += g * Gx[di + 1][dj + 1];
                Gx_b += b * Gx[di + 1][dj + 1];
                Gy_r += r * Gy[di + 1][dj + 1];
                Gy_g += g * Gy[di + 1][dj + 1];
                Gy_b += b * Gy[di + 1][dj + 1];
            }
        }
    }

    // Calculate the final values for each color channel
    int new_r = round(sqrt(Gx_r * Gx_r + Gy_r * Gy_r));
    int new_g = round(sqrt(Gx_g * Gx_g + Gy_g * Gy_g));
    int new_b = round(sqrt(Gx_b * Gx_b + Gy_b * Gy_b));

    // Ensure the final values are within the range [0, 255]
    RGBTRIPLE new_pixel;
    new_pixel.rgbtRed = new_r > 255 ? 255 : new_r;
    new_pixel.rgbtGreen = new_g > 255 ? 255 : new_g;
    new_pixel.rgbtBlue = new_b > 255 ? 255 : new_b;

    return new_pixel;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of the original image to store the new values
    RGBTRIPLE copy[height][width];

    // Iterate over each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute the new pixel value using the Sobel operator
            copy[i][j] = compute_edge_pixel(i, j, height, width, image);
        }
    }

    // Copy the new values back to the original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
}
