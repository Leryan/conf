#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ConfGen(object):
    def __init__(self, nbhosts, svcs_p_host, *args, **kwargs):
        super(ConfGen, self).__init__(*args, **kwargs)
        self.nbhosts = nbhosts
        self.svcs_p_host = svcs_p_host

    def generate(self):
        h_tmpl = """define host {{
    host_name {0}
    alias {0}
    address 127.0.0.1
    use generic-host
    realm {1}
}}
"""
        s_tmpl = """define service {{
    host_name {0}
    service_description {1}
    check_command {2}
    use generic-service
}}
"""

        cfg = []

        for i in range(0, self.nbhosts):
            host_name = 'host_h{0}'.format(i)
            host_cfg = h_tmpl.format(host_name, 'All')
            cfg.append(host_cfg)
            for j in range(0, self.svcs_p_host):
                svc_desc = 'service_h{0}_s{1}'.format(i, j)
                svc_cfg = s_tmpl.format(host_name, svc_desc, 'check_ping')
                cfg.append(svc_cfg)

        return "\n".join(cfg)

if __name__ == '__main__':
    c = ConfGen(300, 10)
    cfg = c.generate()
    print(cfg)
