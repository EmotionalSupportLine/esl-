"""Human Design gates from ecliptic longitude (Rave Mandala).
Gate 41 begins at 302 degrees (2 Aquarius); each gate spans 5.625 degrees, each line 0.9375."""
ORDER = [41,19,13,49,30,55,37,63,22,36,25,17,21,51,42,3,27,24,2,23,8,20,16,35,45,12,15,52,39,53,62,56,
         31,33,7,4,29,59,40,64,47,6,46,18,48,57,32,50,28,44,1,43,14,34,9,5,26,11,10,58,38,54,61,60]
START = 302.0
def gate_of(lon):
    x = (lon - START) % 360
    i = int(x // 5.625)
    line = int((x - i * 5.625) // 0.9375) + 1
    return ORDER[i], line
def gate_start(g):
    return (START + ORDER.index(g) * 5.625) % 360
if __name__ == "__main__":
    # sanity checks: 0 Aries is in Gate 25; 0 Cancer (90) in Gate 15... print a few
    for lon in (0, 90, 180, 270, 302, 3.875):
        print(lon, gate_of(lon))
