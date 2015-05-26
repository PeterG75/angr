import simuvex

class transmit(simuvex.SimProcedure):
    #pylint:disable=arguments-differ

    def run(self, fd, buf, count, tx_bytes):
        if ABSTRACT_MEMORY in self.state.options:
            pos = self.state.posix.get_file(fd)
            data = self.state.mem_expr(buf, count)
            self.state.posix.write(fd, data, count)

            a = simuvex.SimActionData(self.state, 'file', 'write', fd=fd, addr=pos, size=count, data=data)
            self.state.log._add_event(a)

            if self.state.satisfiable(extra_constraints=[tx_bytes != 0]):
                self.state.memory.store(tx_bytes, count)

        else:
            if self.state.satisfiable(extra_constraints=[count != 0]):
                pos = self.state.posix.get_file(fd)
                data = self.state.mem_expr(buf, count)
                self.state.posix.write(fd, data, count)

                a = simuvex.SimActionData(self.state, 'file', 'write', fd=fd, addr=pos, size=count, data=data)
                self.state.log._add_event(a)

            if self.state.satisfiable(extra_constraints=[tx_bytes != 0]):
                self.state.memory.store(tx_bytes, count, condition=tx_bytes != 0)

        # TODO: transmit failure
        return self.state.se.BVV(0, self.state.arch.bits)

from simuvex.s_options import ABSTRACT_MEMORY
