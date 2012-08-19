/**
 * Implements a Disjointed Set Abstract data type.
 */

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace pshin05
{
    class UnionFind
    {
        private int[] cells;     // Array to hold integer objects
        private int[] sizes;     // Number of objects rooted at each cell
        private int[] maxval;    // Maximum element rooted at each cell
        private int numSets;     // Number of disjointed sets

        /* Returns root object */
        private int Root(int i)
        {
            while (cells[i] != i)
            {
                // Apply path compression
                cells[i] = cells[cells[i]];
                i = cells[i];
            }
            return i;
        }

        public UnionFind(int N)
        {
            if (N <= 0) throw new ArgumentException();
            cells = new int[N];
            sizes = new int[N];
            maxval = new int[N];
            numSets = N;

            // Initially all objects has itself as root and max
            for (int i = 0; i < N; i++)
            {
                cells[i] = i;
                maxval[i] = i;
            }
        }

        /* Join two ints in a single set */ 
        public void Union(int i, int j)
        {
            int rooti = Root(i);
            int rootj = Root(j);
            if (rooti == rootj) return;

            // We want the root of the larger tree to be the
            // new root.
            if (sizes[rooti] < sizes[rootj])
            {
                cells[rooti] = rootj;
                sizes[rootj] += sizes[rooti];
                maxval[rootj] = Math.Max(maxval[rooti], maxval[rootj]);
            }
            else
            {
                cells[rootj] = rooti;
                sizes[rooti] += sizes[rootj];
                maxval[rooti] = Math.Max(maxval[rooti], maxval[rootj]);
            }
            // Decrement disj set cout
            numSets--;
        }

        /* Check if two ints are in the same set */
        public bool Connected(int i, int j)
        {
            // Two objects are in the same set if they point
            // to the same root
            return Root(i) == Root(j);
        }

        /* Returns the number of disjointed sets */
        public int Count()
        {
            return numSets;
        }

        /* Returns the largest element in the connected component
         * containing i */
        public int Find(int i)
        {
            return maxval[Root(i)];
        }

        public static void Test()
        {
            UnionFind uf = new UnionFind(10);
            Console.WriteLine("uf.count() is 10: {0}", uf.Count());
            uf.Union(0, 1);
            uf.Union(3, 2);
            Console.WriteLine("uf.count() is 8: {0}", uf.Count());
            Console.WriteLine("uf.connected(0, 1) is true: {0}", uf.Connected(0, 1));
            Console.WriteLine("uf.connected(1, 2) is false: {0}", uf.Connected(1, 2));
            uf.Union(4, 0);
            Console.WriteLine("uf.count() is 7: {0}", uf.Count());
            Console.WriteLine("uf.connected(4, 0) is true: {0}", uf.Connected(4, 0));
            Console.WriteLine("uf.connected(4, 1) is true: {0}", uf.Connected(4, 1));
            uf.Union(5, 6);
            uf.Union(7, 8);
            uf.Union(6, 7);
            uf.Union(2, 5);
            Console.WriteLine("uf.count() is 3: {0}", uf.Count());
            Console.WriteLine("uf.connected(3, 8) is true: {0}", uf.Connected(3, 8));
            Console.WriteLine("uf.connected(3, 0) is false: {0}", uf.Connected(3, 0));
            uf.Union(0, 8);
            Console.WriteLine("uf.count() is 2: {0}", uf.Count());
            Console.WriteLine("uf.connected(3, 0) is true: {0}", uf.Connected(3, 0));
            Console.WriteLine("uf.connected(0, 9) is false: {0}", uf.Connected(0, 9));
            Console.WriteLine("uf.find(0) is 8: {0}", uf.Find(0));
            Console.WriteLine("uf.find(1) is 8: {0}", uf.Find(1));
            Console.WriteLine("uf.find(2) is 8: {0}", uf.Find(2));
            Console.WriteLine("uf.find(3) is 8: {0}", uf.Find(3));
            Console.WriteLine("uf.find(9) is 9: {0}", uf.Find(9));

        }
    }
}
