input_file = "rosalind_ba10c.txt"
with open(input_file) as f:
    data = f.readlines()
seq = data[0].strip()
alphabet = data[2].split()
states = data[4].split()
transitions = {}
for i in range(len(states)):
    src, *probs = data[7+i].split()
    for p, dst in zip(probs, states):
        transitions[(src, dst)] = float(p)
emissions = {}
for i in range(len(states)):
    src, *probs = data[9+len(states)+i].split()
    for p, dst in zip(probs, alphabet):
        emissions[(src, dst)] = float(p)

mat = [[0 for j in range(len(states))] for i in range(len(seq))]
ptr = [[0 for j in range(len(states))] for i in range(len(seq))]

for i, state in enumerate(states):
    mat[0][i] = emissions[state, seq[0]] / len(states)

for i, emission in enumerate(seq[1:], start=1):
    for j, state in enumerate(states):
        opt = [transitions[prev, state] + emissions[state, emission] + mat[i - 1][k] for k, prev in enumerate(states)]
        p = opt.index(max(opt))
        ptr[i][j] = p
        mat[i][j] = max(opt)
ind = max(range(len(state)), key=lambda i: mat[i][-1])
state_seq = states[ind]

while i > 0:
    state_seq = states[ptr[i][ind]] + state_seq
    ind = ptr[i][ind]
    i -= 1
print(state_seq)

