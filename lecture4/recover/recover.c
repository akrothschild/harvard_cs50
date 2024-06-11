#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Define the block size
#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    int file_count = 0;
    FILE *output = NULL;

    // Create a buffer for a block of data
    uint8_t buffer[BLOCK_SIZE];

    // While there's still data left to read from the memory card
    while (fread(buffer, sizeof(uint8_t), BLOCK_SIZE, input) == BLOCK_SIZE)
    {
        // Check if the block indicates the start of a new JPEG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If there's already an open file, close it
            if (output != NULL)
            {
                fclose(output);
            }

            // Create a new filename for the new JPEG file
            char filename[8];
            sprintf(filename, "%03i.jpg", file_count);

            // Open a new file to write the JPEG data
            output = fopen(filename, "w");
            if (output == NULL)
            {
                printf("Could not save file.\n");
                return 1;
            }

            // Increment the file counter
            file_count++;
        }

        // If there is an open file, write the buffer to it
        if (output != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), BLOCK_SIZE, output);
        }
    }

    // Close output file
    if (output != NULL)
    {
        fclose(output);
    }

    // Close the input file
    fclose(input);

    return 0;
}
