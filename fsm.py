class Transitions(object):
    """
    A transition describes what happens in a source state when an event occurs
    src: the current state (str)
    event: what is happening (str)
    condition: a function that must return True for the action or state transition to happen
    action: what to do in case of the event (function)
    dst: the new state after the transition (str)
    """
    def __init__(self):
        self.transitions = {}
    def append(self,src,event,condition=None,action=None,dst=None):
        eventhandler = {}
        if callable(condition): eventhandler['condition'] = condition
        if callable(action): eventhandler['action'] = action
        if dst: eventhandler['dst'] = dst
        self.transitions[(src,event)] = eventhandler
    def run(self,src,event):
        if (src,event) in self.transitions:
            print(event + ' event handler found in ' + src + ' state')
            eventhandler = self.transitions[(src,event)]
            if 'condition' in eventhandler:
                print('Test condition')
                if not eventhandler['condition'](): return src
            if 'action' in eventhandler:
                print('Performing action')
                eventhandler['action']()
            if 'dst' in eventhandler:
                return eventhandler['dst']
        else:
            print('No event handler for ' + event + ' in ' + src + ' state.')
        return src
    def condition(self,src,event):
        try:
            return self.transitions[(src,event)].condition
        except KeyError:
            return None
    def action(self,src,event):
        try:
            return self.transitions[(src,event)].action
        except KeyError:
            return None
    def dst(self,src,event):
        try:
            return self.transitions[(src,event)].dst
        except KeyError:
            return src

class States(object):
    """
    Describe a collection of states for a finit state machine.
    A state has a
    name: The name of the state (str)
    on_entry: A function to be called when entering the state
    on_exit: A function to be called when leaving the state
    """
    def __init__(self):
        self.states = {}
    def append(self, name, on_enter=None, on_exit=None):
        callback_functions = {}
        if callable(on_enter): callback_functions['on_enter'] = on_enter
        if callable(on_exit): callback_functions['on_exit'] = on_exit
        self.states[name] = callback_functions
    def enter(self,name):
        if name in self.states:
            if 'on_enter' in self.states[name]:
                print('Performing on_enter action')
                return self.states[name]['on_enter']()
    def exit(self,name):
        if name in self.states:
            if 'on_exit' in self.states[name]:
                print('Performing on_exit action')
                return self.states[name]['on_exit']()


class Fsm(object):
    """
    A finit state machine described by a list of transitions.
    A transition moves the state machine from one state to another when an event happens
    Transitions can be conditional and can call an external function when they happen
    States are regular strings, but can have enter and exit functions that get called automatically
    """
    def __init__(self, initialstate=None):
        self.state = initialstate
        self.states = States()
        self.transitions = Transitions()

    def append_state(self, name, on_enter=None, on_exit=None):
        self.states.append(name,on_enter,on_exit)

    def append_transition(self, src, event, condition=None, action=None, dst=None):
        self.transitions.append(src,event,condition,action,dst)

    def event(self, event):
        print('Handling ' + event + ' event in ' + self.state + ' state.')
        newstate = self.transitions.run(self.state,event)
        if self.state != newstate:
            self.states.exit(self.state)
            self.states.enter(newstate)
            self.state = newstate
            print('Now in '+ self.state + ' state')
        return self.state
