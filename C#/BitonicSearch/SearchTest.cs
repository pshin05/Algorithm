using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;

namespace BitonicSearch
{
    using NUnit.Framework;

    [TestFixture]
    public class SearchTest
    {
        /* Returns a sorted integer array of given size. */
        private static int[] MakeSortedArray(int size, bool ascend)
        {
            int[] ints = new int[size];
            if (ascend)
            {
                for (int i = 0; i < size; i++)
                    ints[i] = i + 1;
            }
            else
            {
                for (int i = 0; i < size; i++)
                    ints[i] = size - i;
            }
            return ints;
        }

        /* Returns a bitonic array of given size. */
        private static int[] MakeBitonicArray(int size)
        {
            int[] ints = new int[size];
            int mid = (new Random()).Next(size);
            for (int i = 0; i <= mid; i++)
            {
                ints[i] = i + 1;
            }
            for (int i = 0; i < size - mid - 1; i++)
            {
                ints[mid + i + 1] = size - i;
            }
            return ints;
        }

        /* Prints array to console */
        private static void PrintArray(int[] ar)
        {
            foreach (int i in ar)
            {
                System.Console.Write(i);
                System.Console.Write(' ');
            }
            System.Console.WriteLine();
        }

        /**
         * BitonicSearch should work on sorted (either ascending or descending)
         * arrays.
         */
        [Test]
        public void SearchSortedArray()
        {
            for (int i = 1; i <= 10; i++)
            {
                int[] ascending = MakeSortedArray(i, true);
                int[] descending = MakeSortedArray(i, false);
                for (int j = 0; j < i; j++)
                {
                    int result = Search.BitonicSearch(ascending, ascending[j]);
                    Assert.AreEqual(j, result);

                    result = Search.BitonicSearch(descending, descending[j]);
                    Assert.AreEqual(j, result);
                }
            }
        }

        [Test]
        public void SearchBitonicArray()
        {
            for (int i = 1; i <= 20; i++)
            {
                int[] bitonic = MakeBitonicArray(i);
                //PrintArray(bitonic);
                for (int j = 0; j < i; j++)
                {
                    int result = Search.BitonicSearch(bitonic, bitonic[j]);
                    Assert.AreEqual(j, result);
                }
            }
        }

        [Test]
        public void PerformanceTest()
        {
            int size = 1;
            int n = 25;    // Test up to 2^25
            int repeat = 20;
            for (int i = 0; i < n; i++)
            {
                // Take Average of 10 Random Tests
                TimeSpan time = new TimeSpan();
                for (int j = 0; j < repeat; j++)
                {
                    int[] bitonic = MakeBitonicArray(size);
                    int expected = (new Random()).Next(size);
                    Stopwatch watch = new Stopwatch();
                    watch.Start();
                    int result = Search.BitonicSearch(bitonic, bitonic[expected]);
                    watch.Stop();
                    Assert.AreEqual(expected, result);
                    time += watch.Elapsed;
                }
                System.Console.WriteLine("i: {0}, size: {1}, avg time: {2}", 
                    i, size, time.Milliseconds / repeat);

                size *= 2;
            }
        }
    }
}
