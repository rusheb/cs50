// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <string.h>
#include <stdio.h>
#include "helpers.h"

const char *ALL_NOTES[] =  {"C", "C#", "D", "D#", "E", "F",
                            "F#", "G", "G#", "A", "A#", "B"
                           };
const int numNotes = 12;

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int numerator = atoi(strtok(fraction, "/"));
    int denominator = atoi(strtok(NULL, "/"));

    int duration = numerator * 8 / denominator;
    return duration;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    return (
               !strcmp(s, "\r")
               || !strcmp(s, "\n")
               || !strcmp(s, "\r\n")
               || !strcmp(s, "")
           );
}

int getOctave(char *note)
{
    int size = strlen(note);
    int octave = note[size - 1] - '0';
    octave = octave - 4;
    return octave;
}

int getPosition(char *note, int isFlat)
{
    for (int i = 0; i < numNotes; ++i)
    {
        if (strcmp(ALL_NOTES[i], note) == 0)
        {
            if (isFlat)
            {
                return i - 10;
            }
            return i - 9;
        }
    }
    return 0;
}

void getPitch(char *pitch, char *note, int *isFlat)
{
    int size = strlen(note);

    if (size == 3)
    {
        char second = note[1];
        if (second == 'b')
        {
            *isFlat = 1;
            memcpy(pitch, &note[0], 1);
            pitch[1] = '\0';
        }
        else
        {
            memcpy(pitch, &note[0], 2);
            pitch[2] = '\0';
        }
    }
    else if (size == 2)
    {
        memcpy(pitch, &note[0], 1);
        pitch[1] = '\0';
    }

}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    char pitch[3];
    int isFlat = 0;
    getPitch(pitch, note, &isFlat);
    int semitones = getPosition(pitch, isFlat);
    int octave = getOctave(note);
    semitones += octave * 12;

    float hz = 440 * pow(2, ((float) semitones / 12));
    int rounded = (int) round(hz);

    return rounded;
}