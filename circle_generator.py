import random


class CircleMazeGenerator:
    """Generate a perfect maze on concentric rings of equal wedge-shaped cells."""

    def __init__(self, rings, sectors=16):
        self.rings = rings
        self.sectors = sectors
        self.cells = {
            (ring, sector): {"inner": True, "outer": True, "cw": True, "ccw": True, "visited": False}
            for ring in range(rings) for sector in range(sectors)
        }

    def _neighbors(self, ring, sector):
        return [
            ((ring, (sector - 1) % self.sectors), "ccw", "cw"),
            ((ring, (sector + 1) % self.sectors), "cw", "ccw"),
            *((((ring - 1, sector), "inner", "outer"),) if ring > 0 else ()),
            *((((ring + 1, sector), "outer", "inner"),) if ring < self.rings - 1 else ()),
        ]

    def _dfs(self, cell):
        self.cells[cell]["visited"] = True
        ring, sector = cell
        neighbors = self._neighbors(ring, sector)
        random.shuffle(neighbors)
        for other, wall, opposite in neighbors:
            if not self.cells[other]["visited"]:
                self.cells[cell][wall] = False
                self.cells[other][opposite] = False
                self._dfs(other)

    def generate(self):
        self._dfs((0, 0))
        for cell in self.cells.values():
            cell.pop("visited")
        return self.cells
