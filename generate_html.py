import argparse

tab_index_str = """
<div id="page-wrap">
    <a name="tabs"></a>

    <div id="tabs">
        <div id="hiddenbatchid" style="display: none;">${batch_id}</div>

        <div id="hiddenhittype" style="display: none;">${hit_type}</div>

        <div id="hiddendiv" style="display: none;">
            <ul>
                !li_list!
            </ul>
        </div>
"""

irb_str = """
        <!-- Page !page_num! (IRB notice) -->
        <div class="ui-tabs-panel ui-tabs-hide" id="tabs-!page_num!">
            <div class="col-xs-12 col-md-12 col-centered">
                Click "Next Page" to proceed
            </div>
            <div>&nbsp;</div>
            <a class="next-tab mover submit-page" href="#instructions-top" id="!page_num!" rel="!next_page!">Next Page &raquo;</a>
        </div>
        <!-- End Page !page_num! (IRB notice) -->
"""

instructions_str = """
        <!-- Page !page_num! (Instructions) -->
        <div class="ui-tabs-panel ui-tabs-hide" id="tabs-!page_num!">
            <div class="col-xs-12 col-md-12 col-centered">
                Instructions:
            </div>
            <div>&nbsp;</div>
            <a class="next-tab mover submit-page" href="#instructions-top" id="next!page_num!" rel="!next_page!" title="!next_title!">Next Page &raquo;</a>
        </div>
        <!-- End Page !page_num! (Instructions) -->
"""

offer_str = """
        <!-- Page !page_num! (Offer) -->
        <div class="ui-tabs-panel ui-tabs-hide" id="tabs-!tab_num!">
        <h3>If you&#39;d like to continue and perform ${hit_type} additional recipe location tasks for ${offer_amt}, please click &quot;Next Page&quot; below.</h3>
        <h3>Otherwise, click the &quot;Submit&quot; button at the bottom of the page.</h3>
        <div>&nbsp;</div>
        <input type="hidden" name="accepted-!page_num!" id="accepted-!page_num!"/>
        <a class="next-tab mover accept-offer" href="#instructions-top" id="accept-!page_num!" rel="!next_tab!" title="!page_num!">Next Page &raquo;</a></div>
        <!-- End Page !page_num! (Offer) -->
"""

finished_str = """
        <!-- Page !page_num! (Finished) -->

        <div class="ui-tabs-panel ui-tabs-hide" id="tabs-!page_num!">
        <h3>Thank you for completing the HIT! Your additional earnings of ${offer_amt} will be paid via the &quot;bonus&quot; feature. Click the &quot;Submit&quot; button below to finish.</h3>

        <div>&nbsp;</div>
        </div>
        <!-- End Page !page_num! (Finished) -->
"""

def gen_tab_index(first_tasks, second_tasks):
    html_str = tab_index_str
    page_num = 1
    li_list = f"<li><a href=\"#tabs{page_num}\">Consent Form</a></li>\n"
    page_num += 1
    li_list += f"<li><a href=\"#tabs{page_num}\">Demographic Survey</a></li>\n"
    page_num += 1
    task_num = 1
    while task_num <= first_tasks:
        li_list += f"<li><a href=\"#tabs-{page_num}\">Page {page_num} (Stage 1, Task {task_num})</a></li>\n"
        page_num += 1
        task_num += 1
    # Now the Offer
    li_list += f"<li><a href=\"#tabs-{page_num}\">Additional Tasks Offer</a></li>\n"
    page_num += 1
    # And the second round tasks
    while task_num <= (first_tasks + second_tasks):
        li_list += f"<li><a href=\"#tabs-{page_num}\">Page {page_num} (Stage 2, Task {task_num})</a></li>\n"
        page_num += 1
        task_num += 1
    # Finished page
    li_list += f"<li><a href=\"#tabs-27\">Finished</a></li>\n"
    # Now replace the template
    html_str = html_str.replace("!li_list!", li_list)
    return html_str

def gen_irb_html(page_num):
    html_str = irb_str
    html_str = html_str.replace("!page_num!", str(page_num))
    return html_str

def gen_instructions_html(page_num):
    html_str = instructions_str
    html_str = html_str.replace("!page_num!", str(page_num))
    return html_str

def gen_offer_html(page_num):
    html_str = offer_str
    html_str = html_str.replace("!page_num!",str(page_num))
    html_str = html_str.replace("!next_page!",str(page_num + 1))
    return html_str

def gen_task_html(template, page_num, task_num, last_page):
    html_str = template
    html_str = html_str.replace("!page_num!",str(page_num))
    html_str = html_str.replace("!task_num!",str(task_num))
    html_str = html_str.replace("!next_page!",str(page_num + 1))
    html_str = html_str.replace("!next_title!",str(last_page))
    return html_str
  
def gen_finished_html(page_num):
    html_str = finished_str
    html_str = html_str.replace("!page_num!",str(page_num))
    return html_str

def gen_one_stage(num_pages, task_template):
    print(f"One stage with {num_pages} pages")
    one_stage_html = ""
    # IRB page
    # page 1
    one_stage_html += gen_page_html(page_num=1,tab_num=3,next_tab=4,last_tab=num_pages)
    # second stage offer
    one_stage_html += gen_offer_html(page_num=1,tab_num=4,next_tab=5)
    # finished page
    one_stage_html += gen_finished_html(tab_num=27)
    # Save to .txt file
    output_fpath = f"1stage_{num_pages}.html"
    with open(output_fpath, "w", encoding='utf-8') as g:
        g.write(one_stage_html)
    return output_fpath

def gen_two_stage(first_tasks, second_tasks, task_template):
    print(f"Two stage with {first_tasks} tasks in first round and {second_tasks} tasks in second round")
    two_stage_html = ""
    # First, load the headers and instructions sections
    with open("./templates/headers.html", 'r', encoding='utf-8') as f:
        header_html = f.read()
    two_stage_html += (header_html + "\n")
    with open("./templates/instructions.html", 'r', encoding='utf-8') as f:
        instructions_html = f.read()
    two_stage_html += (instructions_html + "\n")
    ### Main part: the tabs
    # 1 page for IRB, 1 page for instructions, N pages for first round, offer page,
    # M pages for second round, then 1 final page telling them that they've completed the task
    # and with a submit button
    total_pages = 1 + 1 + first_tasks + 1 + second_tasks + 1
    # Start with the tab index (necessary for the interface to work)
    two_stage_html += gen_tab_index(first_tasks, second_tasks)
    cur_page = 1
    cur_task_num = 1
    # IRB notice (page 1)
    two_stage_html += gen_irb_html(page_num=1)
    cur_page += 1
    # Instructions (page 2)
    two_stage_html += gen_instructions_html(page_num=2)
    cur_page += 1
    # First round tag panels (starting at page 3)
    last_page_first_stage = cur_page + first_tasks - 1
    while cur_page <= last_page_first_stage:
        cur_task_html = gen_task_html(template=task_template, page_num=cur_page, task_num=cur_task_num,
                                        last_page=total_pages)
        two_stage_html += cur_task_html
        cur_page += 1
        cur_task_num += 1
    # second stage offer
    two_stage_html += gen_offer_html(page_num=cur_page)
    cur_page += 1
    # Second stage tag panels
    last_page_second_stage = cur_page + second_tasks - 1
    while cur_page <= last_page_second_stage:
        cur_task_html = gen_task_html(template=task_template, page_num=cur_page,
                                      task_num=cur_task_num, last_page=total_pages)
        two_stage_html += cur_task_html
        cur_page += 1
        cur_task_num += 1
    # finished page
    two_stage_html += gen_finished_html(page_num=cur_page)
    # Save to .txt file
    output_fpath = f"2stage_{first_tasks}_{second_tasks}.html"
    with open(output_fpath, "w", encoding='utf-8') as g:
        g.write(two_stage_html)
    return output_fpath

def main():
    # Parse command-line args
    parser = argparse.ArgumentParser(description='Generate html code for the monopsony tests.')
    parser.add_argument('--one', type=int, nargs=1, help='number of tasks')
    parser.add_argument('--two', type=int, nargs=2, help='number of tasks for first stage, then number of tasks for second stage')
    args = parser.parse_args()
    #print(args.accumulate(args.integers))
    # Since we don't want to load the page template over and over, load
    # it here and pass to the fns
    with open("./templates/task_pdb.html", 'r', encoding='utf-8') as f:
        task_template = f.read()
    if args.one:
        print(args.one[0])
        output_fpath = gen_one_stage(args.one[0], task_template)
    if args.two:
        print(args.two[0], args.two[1])
        output_fpath = gen_two_stage(args.two[0], args.two[1], task_template)
    print(f"Generated html saved to {output_fpath}")

if __name__ == "__main__":
    main()