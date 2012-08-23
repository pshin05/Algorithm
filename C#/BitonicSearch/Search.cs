using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

/**
 * Bitonic Array consists of an increasing sequence of integers
 * followed immediately by decreasing sequence of integers.
 * Bitonic search algorithm searches for a specific item in
 * O(log N) time.
 * 
 * Basic search strategy:
 * When we select the middle term and compare it to the term immediately to
 * the left (left) and the term to the immediately to the right (right), one
 * of the following 3 cases must be true.
 * 1. left < mid < right
 * 2. left > mid > right
 * 3. left < mid > right
 * (Note that left > mid < right case is impossible)
 * 
 * For case 1, the array on [start, left] must be sorted and ascending.
 * Thus, we check if target < mid, and if so we perform binary search on 
 * [start, left] and return the index if item is found. Otherwise we make a
 * tail recusive call to BitonicSearch on [right, end].
 * 
 * For case 2, the array on [right, end] must be sorted and descending.
 * Thus, we check if target < mid, and if so we perform binary search on
 * [right, end] and return the result if item is found. Otherwise we make a
 * tail recusive call to BitonicSearch on [start, left].
 * 
 * For case 3, the array on [start, left] must be sorted and ascending, and
 * the array on [right, end] must be sorted and descending. If target > mid,
 * we return -1; otherwise we perform consecutive binary searches on these 
 * intervals until match is found.
 */

namespace BitonicSearch
{
    class Search
    {
        /**
         * Search for target item in the bitonic array.
         * Returns the index of the array location, or -1
         * if the target is not found.
         */
        public static int BitonicSearch(int[] bitonic, int target)
        {
            return BitonicSearchRange(bitonic, 0, bitonic.Length, target);
        }

        /**
         * Performs binary search on the portion of the array known to 
         * be sorted (either ascending or descending).
         * "start" range index is inclusive, whereas "end" index is exclusive.
         */
        private static int BinarySearchRange(int[] ar, int start, int end, int target, bool ascend)
        {
            // Base case
            if (start >= end)
                return -1;

            // Compare with middle item
            int mid = (end - start) / 2;
            if (target == ar[mid])
                return mid;

            // Perform BinarySearch recursively on an interval half as long.
            if ((ascend && target < ar[mid]) || (!ascend && target > ar[mid]))
                return BinarySearchRange(ar, start, mid - 1, target, ascend);
            else
                return BinarySearchRange(ar, mid + 1, end, target, ascend);
        }

        /**
         * Searchs for given target within given range.
         * Returns the index of the target within the array or -1 if not found.
         * "start" range index is inclusive, whereas "end" index is exclusive.
         */
        private static int BitonicSearchRange(int[] ar, int start, int end, int target)
        {
            // Trivial case
            if (start >= end) 
                return -1;

            // If less than 3 elements, check for match one by one.
            if (start + 2 <= end)
            {
                while (start < end)
                {
                    if (target == ar[start])
                        return start;
                    start++;
                }
                return -1;
            }

            // Check middle item; Note that we're assured that there is at least
            // one element at each side of the middle item.
            int mid = (end - start) / 2;
            if (target == ar[mid])
                return mid;
            
            if (ar[mid-1] < ar[mid] && ar[mid] < ar[mid+1])
            {
                // Case 1
                int found = -1;
                if (target < ar[mid])
                {
                    found = BinarySearchRange(ar, start, mid - 1, target, true);
                }
                if (found != -1)
                    return found;
                else
                    return BitonicSearchRange(ar, mid + 1, end, target);
            }
            else if (ar[mid - 1] > ar[mid] && ar[mid] > ar[mid + 1])
            {
                // Case 2
                int found = -1;
                if (target < ar[mid])
                {
                    found = BinarySearchRange(ar, mid + 1, end, target, false);
                }
                if (found != -1)
                    return found;
                else
                    return BitonicSearchRange(ar, start, mid - 1, target);
            }
            else if (ar[mid - 1] < ar[mid] && ar[mid] > ar[mid + 1])
            {
                // Case 3 (This case applies at most one time during a search)
                int found = -1;
                if (target > ar[mid])
                    return -1;
                found = BinarySearchRange(ar, start, mid - 1, target, true);
                if (found != -1)
                    return found;
                else
                    return BinarySearchRange(ar, mid + 1, end, target, false);
            }
            else
            {
                throw new ArgumentException("Array is not bitonic");
            }
        }
    }
}
